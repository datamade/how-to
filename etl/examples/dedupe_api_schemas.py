from functools import wraps
import json
import re

from marshmallow import Schema, fields, ValidationError, pre_load, post_load, \
    validate, validates

import sqlalchemy as sa
from sqlalchemy.exc import DataError
from sqlalchemy.orm.exc import NoResultFound

from api.cogs.common_utils import engine_manager
from api.database import db
from api.exceptions import WebAPIAccessDeniedException
from api.models import DedupeProject, User


class UUIDString(fields.UUID):
    def _validated(self, value):
        '''
        Only accept UUIDs, but load them as strings.
        '''
        value = super()._validated(value)
        return str(value)


class AuthenticationMixin:
    def authenticate_request(self, in_data, project=True):
        user = self.retrieve_user(in_data)

        try:
            any_api_access = any(g.api_access for g in user.groups)

            assert any_api_access
        except AssertionError:
            message = 'Sorry, your account does not have permission to use the Dedupe.io API. Email info@dedupe.io to request access.'
            raise WebAPIAccessDeniedException(message, status_code=403)

        if project:
            project = self.retrieve_project(in_data)

            # Handle case where the user belongs to multiple groups
            # but tries to operate on a project for a group without
            # API access.
            try:
                assert project.group.api_access
            except AssertionError:
                message = 'Sorry, your account does not have permission to use the Dedupe.io API with this project. Email info@dedupe.io to request access.'
                raise WebAPIAccessDeniedException(message, status_code=403)

            try:
                assert project.group in user.groups
            except AssertionError:
                message = 'Sorry, you do not have access to this project'
                raise WebAPIAccessDeniedException(message, status_code=403)

        else:
            project = None

        return user, project

    def retrieve_project(self, in_data):
        try:
            project_id = in_data['project_id']
        except KeyError:
            message = 'You must provide a project ID to use the API'
            raise WebAPIAccessDeniedException(message, status_code=400)

        try:
            return db.session.query(DedupeProject)\
                             .filter(DedupeProject.id == project_id)\
                             .one()

        except NoResultFound:
            message = 'Sorry, a project with ID "{}" cannot be found'.format(project_id)
            raise WebAPIAccessDeniedException(message, status_code=404)

        except DataError:
            message = 'Sorry, "{}" is not a valid project ID'.format(project_id)
            raise WebAPIAccessDeniedException(message, status_code=400)

    def retrieve_user(self, in_data, **kwargs):
        try:
            user_id = in_data['api_key']
        except KeyError:
            message = 'You must provide an API key to use the API'
            raise WebAPIAccessDeniedException(message, status_code=401)

        try:
            return db.session.query(User).filter(User.id == user_id).one()
        except (NoResultFound, DataError):
            message = 'Sorry, "{}" is not a valid API key'.format(user_id)
            raise WebAPIAccessDeniedException(message, status_code=401)


class RequestSchema(AuthenticationMixin, Schema):
    api_key = UUIDString(required=True)

    @pre_load
    def preprocess(self, in_data, **kwargs):
        '''
        See pattern:
        https://marshmallow.readthedocs.io/en/latest/extending.html#pre-post-processor-invocation-order
        '''
        if isinstance(in_data, bytes):
            in_data = self.load_from_bytestring(in_data)

        self.user, self.project = self._authenticate(in_data)

        return in_data

    def load_from_bytestring(self, in_data):
        try:
            return json.loads(in_data.decode('utf-8'))
        except:
            message = 'The content of your request should be a string encoded JSON object'
            raise ValidationError(message)

    def _authenticate(self, in_data):
        return self.authenticate_request(in_data, project=False)


class ProjectListRequestSchema(RequestSchema):

    ORDER_BY_OPTIONS = (
        'name',
        'date_added',
    )

    order_by = fields.String(validate=validate.OneOf(ORDER_BY_OPTIONS))
    descending = fields.Boolean()


class ProjectRequestSchema(RequestSchema):
    project_id = UUIDString(required=True)

    @validates('project_id')
    def validate_project(self, value):
        if not self.project.is_canonical:
            message = 'There are datasets in the project with ID "{}" that are still being processed'.format(value)
            raise ValidationError(message)

        elif all(ds.precanonical for ds in self.project.datasets):
            message = 'You must use dedupe.io to deduplicate a dataset in the project with ID "{}" before you can use the API'.format(value)
            raise ValidationError(message)

    def _authenticate(self, in_data):
        return self.authenticate_request(in_data)


class RetrainRequestSchema(ProjectRequestSchema):
    pass


class ObjectRequestSchema(ProjectRequestSchema):
    object = fields.Dict(required=True)
    dataset_id = UUIDString()

    @validates('object')
    def validate_object(self, value, **kwargs):
        object_schema = self._make_object_schema()

        # If there is not a schema, skip object validation. An exception will be
        # raised by project validation.
        if object_schema:
            try:
                object_schema.load(value)
            except ValidationError:
                raise

    @post_load
    def postprocess(self, in_data, **kwargs):
        '''
        TODO: If objects have a "record_id" key, that key should be transformed
        into "user_record_id" for both raw and processed objects to avoid
        collisions.
        '''
        abstract_record = self._make_abstract_record(in_data['object'])
        in_data['processed_object'] = self._make_processed_record(abstract_record)
        return in_data

    def _make_object_schema(self, match=False):
        field_defs = self.project.field_defs

        if field_defs:
            schema_dict = {
                self._strip_abs_prefix(field['field']): fields.Raw(allow_none=True, required=True)
                for field in self.project.field_defs
            }

            if match:
                schema_dict.update({
                    'match': fields.Int(validate=validate.Range(min=0, max=1), required=True),
                    'record_id': fields.Int(allow_none=False),
                })

            return Schema.from_dict(schema_dict)()

    def _make_abstract_record(self, object):
        return {'abs_{}'.format(k): v for k, v in object.items()}

    def _make_processed_record(self, object):
        processed_record = {}

        for k, v in object.items():
            if isinstance(v, str):
                v = v.lower().strip()

                if v == '':
                    v = None

            processed_record[k] = v

        return processed_record

    def _strip_abs_prefix(self, string):
        return re.sub(r'^abs_', '', string, count=1)


class MatchRequestSchema(ObjectRequestSchema):
    threshold = fields.Float()


class TrainRequestSchema(ObjectRequestSchema):
    matches = fields.List(fields.Dict(), required=True)

    class Decorators(object):
        @classmethod
        def match_processor(self, f):
            @wraps(f)
            def wrapper(self, object, **kwargs):
                '''
                Remove metadata (record ID and whether the object is a match)
                from match objects before processing them. Add it back after.
                '''
                copied_object = object.copy()

                cache = {
                    'record_id': copied_object.pop('record_id', None),
                    'match': copied_object.pop('match', None),
                }

                processed_object = f(self, copied_object, **kwargs)

                for key, value in cache.items():
                    if value is not None:
                        processed_object[key] = value

                return processed_object

            return wrapper

    @validates('matches')
    def validate_matches(self, value, **kwargs):
        match_schema = self._make_object_schema(match=True)

        # If there is not a schema, skip match validation. An exception will be
        # raised by project validation.
        if match_schema:
            errors = []

            for match in value:
                try:
                    match_schema.load(match)
                except ValidationError as e:
                    errors.append(str(e))

            if errors:
                raise ValidationError(errors)

    @post_load
    def postprocess(self, in_data, **kwargs):
        in_data = super().postprocess(in_data, **kwargs)

        processed_matches = []

        for match in in_data['matches']:
            abstract_match = self._make_abstract_match(match)
            processed_matches.append(self._make_processed_match(abstract_match))

        in_data['processed_matches'] = processed_matches

        return in_data

    @Decorators.match_processor
    def _make_abstract_match(self, object):
        return self._make_abstract_record(object)

    @Decorators.match_processor
    def _make_processed_match(self, object):
        return self._make_processed_record(object)


class AddRequestSchema(ObjectRequestSchema):
    cluster_id = UUIDString()

    @validates('cluster_id')
    def validate_cluster_id(self, value, **kwargs):
        entity_map = 'change_log_{}'.format(self.project.id)

        entity_query = '''
            SELECT EXISTS(
              SELECT 1 FROM "{entity_map}"
              WHERE entity_id = :entity_id
            )
        '''.format(entity_map=entity_map)

        with engine_manager() as engine:
            entity = engine.execute(
                sa.text(entity_query),
                entity_id=value
            ).first()

        try:
            assert entity.exists

        except AssertionError:
            raise ValidationError('Provided cluster_id does not exist.')
