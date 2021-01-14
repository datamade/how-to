# 🍪 Containerization templates

This directory contains [cookiecutters](https://github.com/audreyr/cookiecutter)
for the containerization of web applications.

## Getting started

### 1. Set up.

Clone this repository to your favorite working directory –

```bash
git clone https://github.com/datamade/how-to.git && cd how-to/docker/templates
```

– and build or update your template image.

```bash
docker-compose build
```

### 2. Run `cookiecutter`.

To run cookiecutter on a specific template, you can run `cookiecutter -f path/to/template/dir`.
So, to **generate a new Django project**, use Docker to run cookiecutter with the `new-django-app/` directory
as a target:

```bash
docker-compose run --rm cookiecutter -f new-django-app
```

To generate a Docker environment for an **existing Python project**, use the
`python-docker-env` directory as a target:

```bash
docker-compose run --rm cookiecutter -f python-docker-env
```

#### Template variables

When you run `cookiecutter`, it will ask you to define some or all of the following variables
in your terminal:

| Variable | Definition |
| - | - |
| `directory_name` | The directory that will contain your generated files. We'll move the files out and remove this directory after running `cookiecutter` so it's fine to use the default here. |
| `app_name` | The slug you use to refer to your application (typically the same as the GitHub repo). |
| `app_verbose_name` | A verbose name for your application, written in plain English and typically title-case (e.g. "BGA Pensions Database"). |
| `module_name` | The slug you use to refer to the Python module that contains your app. In contrast to `app_name`, this variable must be a valid Python module name, e.g. underscores are permitted while spaces/hyphens are not. |
| `local_settings` | If your project includes a local settings file, set this equal to the relative path to your local settings file (or your example settings file, if it includes working values), and it will be automatically mounted into your application container. Set this to the string `None` if your application does not use a local settings file. |
| `run_command` | The command to run your application. |
| `migrate_command` | The command to migrate your database. |
| `auto_migrate` | Whether your database migration should be run every time you start your application. Set this to False if you have a workflow that involves loading in a database dump. Note that you will need to run migrations manually thereafter, e.g., `docker-compose exec app python manage.py migrate`. |
| `postgis` | Whether to use the Postgis image. |
| `pg_version` | The version of the Postgres or Postgis image you'd like to use. |
| `pg_db` | The name of your database. |

### 3. Move generated files to the right location.

Once you've generated your files, you'll need to move them out of the `how-to/docker/templates`
directory and into whatever repo needs to use them.

If you're generating a Django app using **the `new-django-app` template**, typically you'll
need to move the new directory you generated to be a sibling of the `how-to`
directory (i.e. move it to wherever you store your DataMade projects). Then, change
into the new directory and initialize it as a Git repo with `git init`:

```bash
# Replace ${directory_name} with the name of the directory you just set
# If you used the default, it's my-new-app
mv ${directory_name} ../../..
cd ../../../${directory_name} && git init
```

If you're generating a Docker environment for an existing
app using **the `python-docker-env` template**, you'll need to move the files you generated to
the repo that stores the existing project. For example:

```bash
# Replace ${directory_name} with the name of the directory you just set
# If you used the default, it's my-docker-env
rsync -av ${directory_name}/* /path/to/existing/project && rm -rf ${directory_name}/
```

Note that this will preserve `configs/` and `scripts/` directories and their
contents, if your project already contains them.

### 4. Customize your configs and scripts.

The templated configs were written to serve our most common use cases.
Sometimes, though, your deployment may require changes or additions to the
boilerplate files. Perhaps you need to mount additional volumes in your Docker
config, or define an extra service, e.g., Redis for queueing or Solr for search.

For Django apps produced with the `new-django-app` template, you'll always want to at least
pin the requirements in `requirements.txt` to the latest available versions. We
recommend [`pip chill`](https://github.com/rbanffy/pip-chill) for this task:

```bash
# Run this on your host machine to spawn a shell in an app container
$ docker-compose run --rm app bash

# Run this inside the spawned app container
~ pip-chill | grep -v pip-chill > requirements.txt
```

You may need to make other adjustments; refer to [the Django
docs](https://docs.djangoproject.com/en/stable/intro/tutorial01/) for more
on project setup.

If you need to make a customization and aren't sure how to start, check in with
a Lead Developer. Chances are we've made that customization before and can
refer you to an example project.

### 5. Run your application!

Change to your application directory, run `docker-compose up -d` to build your
application and its services, then go to localhost:8000 (or whatever port you defined
in the run command) to view your containerized app.

See [Using your `docker-compose` setup](../local-development.md#using-your-docker-compose-setup)
for more on local development with Docker.
