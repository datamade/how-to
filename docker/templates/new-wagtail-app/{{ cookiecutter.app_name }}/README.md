# {{ cookiecutter.app_verbose_name }}

## Developing

### Set-up pre-commit

We use the [pre-commit](https://pre-commit.com/) framework to use Git pre-commit hooks that keep our codebase clean.

To set up Pre-Commit, install the Python package on your local machine using

```bash
python -m pip install pre-commit
```

If you'd rather not install pre-commit globally, create and activate a [virtual environment](https://docs.python.org/3/library/venv.html) in this repo before running the above command.

Then, run

```bash
pre-commit install
```

to set up the git hooks.

Since hooks are run locally, you can modify which scripts are run before each commit by modifying `.pre-commit-config.yaml`.


### Docker

Development requires a local installation of [Docker](https://docs.docker.com/install/)
and [Docker Compose](https://docs.docker.com/compose/install/).

Before building the Docker container, copy over the .env settings
```bash
cp env.example .env
```

Build the app and run it to trigger migrations:

```bash
docker-compose up --build
```

To populate the starter content for the CMS, run:

```bash
docker-compose run --rm app python manage.py load_cms_content
```

Run the app:

```bash
docker-compose up
```

The app will be available at http://localhost:8000. The database will be exposed
on port 32001.


### Admin

You can access the Wagtail admin interface at http://localhost:8000/admin and the 
Django admin interface at http://localhost:8000/django-admin.

The default admin account credentials are located in the DataMade LastPass.


### Running tests

Run tests with Docker Compose:

```bash
docker-compose -f docker-compose.yml -f tests/docker-compose.yml run --rm app
```


## For the designers: styles, images and templates

When working on the styles, images and templates for this site, here are the places you'll want to add your stuff:

* Templates: Located in `{{ cookiecutter.module_name }}/templates/{{ cookiecutter.module_name }}/` and use the [Django template language](https://docs.djangoproject.com/en/3.2/topics/templates/). `base.html` is the base page template, which contain the header and footer. 
* CSS: This site uses [Bootstrap 4.6](https://getbootstrap.com/docs/4.6/getting-started/introduction/) for its base sytles. All additional style customizations should be placed in `{{ cookiecutter.module_name }}/static/css/custom.css`
* Javascript: This site uses [React 17.0.2](https://reactjs.org/), [jQuery 3.6](https://jquery.com/) and [Bootstrap 4.6](https://getbootstrap.com/docs/4.6/getting-started/javascript/). Custom javascript should be placed in `{{ cookiecutter.module_name }}/static/js/base.js`.
* Icons: This site makes use of the free icon set from [Fontawesome 5.11](https://fontawesome.com/icons?d=gallery&p=2&m=free), which can be [used directly in any templates](https://fontawesome.com/how-to-use/on-the-web/referencing-icons/basic-use).

## Initial CMS content

This template does not include a default user or starter pages in the fixtures directory, so you'll need 
to create an admin user and initialize initial content as needed by your site:

```bash
docker-compose run --rm app python manage.py createsuperuser
```

**To create a new dump** of all the content in the Wagtail backend, perform the following steps:

1. Back up the CMS content (except for image files) with the following 2 commands:

    ```bash
    docker-compose run --rm app python manage.py dumpdata --natural-foreign --indent 2 \
        --exclude={{ cookiecutter.module_name }} \
        --exclude=contenttypes \
        --exclude=auth.permission \
        --exclude=wagtailcore.groupcollectionpermission \
        --exclude=wagtailcore.grouppagepermission \
        --exclude=sessions -o {{ cookiecutter.module_name }}/fixtures/initial_cms_content.json
    ```

    ```bash
    docker-compose run --rm app python manage.py dumpdata --natural-foreign --indent 2 \
        {{ cookiecutter.module_name }}.homepage \
        {{ cookiecutter.module_name }}.staticpage \
        -o {{ cookiecutter.module_name }}/fixtures/initial_cms_content_custom_pages.json
    ```

    This should update the `initial_cms_content.json` file in your `{{ cookiecutter.module_name }}/fixtures`
    directory.

2. Copy over images

```bash
cp -R media/. {{ cookiecutter.module_name }}/fixtures/initial_images/
```

This will update the default image files by copying your local Wagtail images folder into `fixtures/initial_images`. This directory is copied to your media root directory by the `load_cms_content` management command.


**To back up content from a site on Heroku**, run the same above commands using the `heroku run` command:

```bash
    heroku run -a {{ cookiecutter.module_name }}-staging python manage.py dumpdata --natural-foreign --indent 2 \
    --exclude={{ cookiecutter.module_name }} \
    --exclude=contenttypes \
    --exclude=auth.permission \
    --exclude=wagtailcore.groupcollectionpermission \
    --exclude=wagtailcore.grouppagepermission \
    --exclude=sessions > {{ cookiecutter.module_name }}/fixtures/initial_cms_content.json
```

```bash
    heroku run -a {{ cookiecutter.module_name }}-staging python manage.py dumpdata --natural-foreign --indent 2 \
    {{ cookiecutter.module_name }}.homepage \
    {{ cookiecutter.module_name }}.staticpage \
    > {{ cookiecutter.module_name }}/fixtures/initial_cms_content_custom_pages.json
```

