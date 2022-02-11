# {{ cookiecutter.app_name }}

## Cookiecutter Notes

### Preparing for Docker

Before building the Docker container, initialize the database:

```bash
docker-compose run --rm app python manage.py makemigrations
```

```bash
docker-compose run --rm app python manage.py migrate
```
### Initial Docker Run

When running `docker-compose up` for the first time, you may run into a database connection
error that causes Docker to hang. Simply force quit Docker with `Ctrl-C` and re-run
`docker-compose up`.

### Initial Wagtail CMS Content

The `fixtures/` directory has been intentionally left empty. Including `initial_cms_content.json`
and `initial_cms_content_custom_pages.json` would require creating a Django admin account
in advance which would introduce a security vulnerability if the admin password was not
updated.

After initializing the database, follow the instructions below to generate the initial CMS content.

Note: Because the initial CMS content is created using stdout, it may include extra content
at the top of the file. After creating `initial_cms_content.json` and `initial_cms_content_custom_pages.json`,
check the files. Simply remove any stdout text that precedes the opening bracket of the
CMS content list.


## Developing

Development requires a local installation of [Docker](https://docs.docker.com/install/)
and [Docker Compose](https://docs.docker.com/compose/install/).

Build application containers:

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

### Running tests

Run tests with Docker Compose:

```bash
docker-compose -f docker-compose.yml -f tests/docker-compose.yml run --rm app
```

## Creating CMS users

To access the Wagtail CMS at http://localhost:8000/admin, you will need to create a login:

```bash
docker-compose run --rm app python manage.py createsuperuser
```

## For the designers: styles, images and templates

When working on the styles, images and templates for this site, here are the places you'll want to add your stuff:

* Templates: Located in `{{ cookiecutter.module_name }}/templates/{{ cookiecutter.module_name }}/` and use the [Django template language](https://docs.djangoproject.com/en/3.2/topics/templates/). `base.html` is the base page template, which contain the header and footer. 
* CSS: This site uses [Bootstrap 4.6](https://getbootstrap.com/docs/4.6/getting-started/introduction/) for its base sytles. All additional style customizations should be placed in `{{ cookiecutter.module_name }}/static/css/custom.css`
* Javascript: This site uses [jQuery 3.6](https://jquery.com/) and [Bootstrap 4.6](https://getbootstrap.com/docs/4.6/getting-started/javascript/). Custom javascript should be placed in `{{ cookiecutter.module_name }}/static/js/base.js`.
* Icons: This site makes use of the free icon set from [Fontawesome 5.11](https://fontawesome.com/icons?d=gallery&p=2&m=free), which can be [used directly in any templates](https://fontawesome.com/how-to-use/on-the-web/referencing-icons/basic-use).

## Initial CMS content

**To create a new dump** of all the content in the Wagtail backend, perform the following steps:

1. Back up the CMS content (except for image files) with the following 2 commands:

    ```bash
    docker-compose run --rm app python manage.py dumpdata --natural-foreign --indent 2 \
        --exclude={{ cookiecutter.module_name }} \
        --exclude=contenttypes \
        --exclude=auth.permission \
        --exclude=wagtailcore.groupcollectionpermission \
        --exclude=wagtailcore.grouppagepermission \
        --exclude=sessions > {{ cookiecutter.module_name }}/fixtures/initial_cms_content.json
    ```

    ```bash
    docker-compose run --rm app python manage.py dumpdata --natural-foreign --indent 2 \
        {{ cookiecutter.module_name }}.homepage \
        {{ cookiecutter.module_name }}.staticpage \
        > {{ cookiecutter.module_name }}/fixtures/initial_cms_content_custom_pages.json
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
