# Based on the Wagtail demo:
# https://github.com/wagtail/bakerydemo/blob/master/bakerydemo/base/management/commands/load_initial_data.py
import os
import json

from django.files.storage import default_storage
from django.apps import apps
from django.management.base import BaseCommand
from django.management import call_command
from django.exceptions import ObjectDoesNotExist

from wagtail.models import Site, Page, PageRevision
from wagtail.images.models import Image


class Command(BaseCommand):

    @property
    def fixtures_dir(self):
        project_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
        return os.path.join(project_dir, 'fixtures')

    def add_arguments(self, parser):
        parser.add_argument(
            '--content-type',
            default='models',
            type=lambda x: x.split(','),
            help='Comma-separated string of content types to load. Default: \
                  models. Options: models, images.'
        )

    def handle(self, **options):
        selected_content = set(options['content_type'])
        valid_content = set(['models', 'images'])

        if not selected_content.issubset(valid_content):
            invalid_values = selected_content - valid_content
            raise ValueError('Invalid content types: {}. Valid options are: \
                              models, images'.format(invalid_values))

        else:
            for content in options['content_type']:
                getattr(self, 'load_{}'.format(content))()

    def load_models(self):
        initial_data_file = os.path.join(self.fixtures_dir, 'initial_cms_content.json')
        initial_data_file_custom_pages = \
            os.path.join(self.fixtures_dir,
                         'initial_cms_content_custom_pages.json')

        with open(initial_data_file) as f:
            initial_data = json.load(f)

        if initial_data:
            # Delete existing Wagtail models
            try:
                Site.objects.all().delete()
                Page.objects.all().delete()
                PageRevision.objects.all().delete()
                Image.objects.all().delete()

                for Model in apps.get_app_config('{{ cookiecutter.module_name }}').get_models():
                    if getattr(Model, 'reset_on_load', False):
                        Model.objects.all().delete()

            except ObjectDoesNotExist as e:
                self.stdout.write(self.style.WARNING(e))

            call_command('loaddata', initial_data_file, verbosity=0)
            call_command('loaddata', initial_data_file_custom_pages, verbosity=0)

            self.stdout.write(self.style.SUCCESS('Initial data loaded!'))
        else:
            self.stdout.write(self.style.NOTICE('No initial data!'))

    def load_images(self):
        initial_images_dir = os.path.join(self.fixtures_dir, 'initial_images')

        for root, dirs, files in os.walk(initial_images_dir):

            for filename in files:
                source_path = os.path.join(root, filename)
                dest_path = os.path.relpath(source_path, initial_images_dir)

                if default_storage.exists(dest_path):
                    self.stdout.write(
                        self.style.WARNING(
                            '{} aleady exists. Skipping...'.format(dest_path)
                        )
                    )
                    continue

                else:
                    with open(source_path, 'rb') as img:
                        default_storage.save(dest_path, img)
                    self.stdout.write(
                        self.style.SUCCESS(
                            'Copied {} to default storage'.format(dest_path)))

        self.stdout.write(self.style.SUCCESS('Copied all initial images!'))
