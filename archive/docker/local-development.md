# Docker for Local Development

Docker for local development was piloted on `dedupe-service`, a repository to
which some DataMade employees do not have access. Luckily, we have since applied
the pattern to other projects. Some examples in the wild:

- [🏡 `ihs-website-v2`](https://github.com/datamade/ihs-website-v2)
- [🏆 `lisc-cdna`](https://github.com/datamade/lisc-cnda)

## Core concepts

If you're new to Docker, the glut of blog posts, articles, and third-party
documentation can be a lot to parse through. We recommend starting with
Docker's own explanations of the fundamental building blocks of containers.

- [Image](https://docs.docker.com/glossary/?term=image)
- [Container](https://docs.docker.com/glossary/?term=container)
- [Volume](https://docs.docker.com/glossary/?term=volume)
- [Service](https://docs.docker.com/glossary/?term=service)
- [Compose](https://docs.docker.com/glossary/?term=Compose)

The Docker documentation also includes an [Get started](https://docs.docker.com/get-started/)
tutorial that can help connect the dots between these concepts. Give it a whirl
(or at least a scan)!

## Overview

A containerized local development environment has a few components, including
some optional configurations and services:

1. [A Dockerfile](#1-dockerfile), containing building instructions for the application itself.
2. [A root `docker-compose.yml` file](#2-docker-composeyml)
that declares the application and its dependent services
3. [A `tests/docker-compose.yml` file](#3-testsdocker-composeyml)
that overrides the application service in the root file, in order to run the tests
4. [A `.env` file](#4-env-optional) that sets secret values to be threaded into
your app at runtime (Optional)
5. [A database initialization script](#5-scriptsinit-dbsh-optional)
that creates your database and installs any extensions (Optional)
6. [A `docker-compose.db-ops.yml` file](#6-docker-composedb-opsyml-optional)
that automates a multi-step data loading routine (Optional)

The required components of a containerized setup for local development are
templated for reuse in the `templates/` directory. See [the README](templates/README.md)
for instructions for use.

With this setup, you can:

- [Run your application or tests](#run-the-application)
- [Access the `pdb` shell](#docker-and-pdb)
- [Run custom commands on your container](#run-custom-commands-on-containers)
- [Install a local installation of a Python package for development](#install-a-local-installation-of-a-python-package-for-development)

If you run into trouble, see [Debugging your containerized setup](#debugging-your-containerized-setup).

## Components

### 1. `Dockerfile`

📄 [`Dockerfile`](templates/python-docker-env/{{cookiecutter.directory_name}}/Dockerfile)

### 2. `docker-compose.yml`

📄 [`docker-compose.yml`](templates/python-docker-env/{{cookiecutter.directory_name}}/docker-compose.yml)

There are [several versions](https://docs.docker.com/compose/compose-file/compose-versioning/)
of `docker-compose` syntax. We prefer v2, in order to take advantage of health
checks and expressive `depends_on` declarations. This allows us to delay the
start of an application until the services it needs have finished building.

v3 no longer supports this syntax. More on that [in this issue](https://github.com/peter-evans/docker-compose-healthcheck/issues/3#issuecomment-329037485).

### 3. `tests/docker-compose.yml`

📄 [`tests/docker-compose.yml`](templates/python-docker-env/{{cookiecutter.directory_name}}/tests/docker-compose.yml)

### 4. `.env` (Optional)

Docker Compose offers [many ways](https://docs.docker.com/compose/environment-variables/)
to thread variables into your containers. We like to use the `environment` key
to set non-sensitive config values, such as local database connections, for
services in `docker-compose.yml`.

If your application includes sensitive config values, it's good practice to
define null fallbacks if your application doesn't require them for local
development.

**Example `settings.py`**

```python
import os


API_KEY = os.getenv('API_KEY', '')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
```

If you do need to interact with a third-party service during local development,
define a `.env` file in your project root containing those config values. Be
sure to exclude it in your `.gitignore` file to avoid committing secrets!

**Example `.env`**

```bash
API_KEY="some key"
EMAIL_PASSWORD="some password"
```

Docker Compose will [automatically thread variables defined in `.env` into your
containers](https://docs.docker.com/compose/environment-variables/#the-env-file).
We like this approach because:

- It's directly analogous to our [Heroku deployment environment](https://github.com/datamade/how-to/blob/master/heroku/deploy-a-django-app.md#read-settings-and-secret-variables-from-the-environment),
so we can use our existing configuration files.
- It's easy to exclude `.env` files from version control, so you don't have to
remember to remove sensitive values from `docker-compose.yml` or your settings
files before you save your changes.

Need to share credentials with other members of the DataMade team? Store them
in our shared LastPass folder.

### 5. `scripts/init-db.sh` (Optional)

The default Postgres image exposes [a number of environment variables](https://hub.docker.com/_/postgres/#environment-variables)
that allow you to define custom behavior for your container without writing
additional code. Things you can achieve via environment variables include
creating your default database, specifying a default user and password, and
customizing the location of the database files.

If you need more advanced functionality, e.g., installing a custom Postgres
extension, the Postgres image provides a harness for executing arbitrary SQL
and Bash scripts when a container is initialized. [Read more. &raquo;](https://docs.docker.com/samples/library/postgres/#initialization-scripts)

```bash
#!/bin/bash
set -e

psql -U postgres -c "CREATE DATABASE ${YOUR_DATABASE}"
psql -U postgres -d ${YOUR_DATABASE} -c "CREATE EXTENSION IF NOT EXISTS ${YOUR_EXTENSION}"
# Add any more database initialization commands you may need here
```

If you define a custom database initialization script, be sure to mount it
as a volume in your Postgres container in `docker-compose.yml`.

```yml
    volumes:
      - ...
      # Assuming script lives in scripts/init-db.sh
      - ${PWD}/scripts/init-db.sh:/docker-entrypoint-initdb.d/10-init.sh
```

***If you would like to use the Postgis extension,*** we recommend using a
Postgis image, rather than configuring it in an initialization script.

### 6. `docker-compose.db-ops.yml` (Optional)

Data-rich applications may come with a multi-step process for loading in data.
In those instances, it can be helpful to define a service that automates each
of those steps, so initializing your application is a breeze.

Define this, in _addition_ to a `migration` service, because you will always
want to capture migrations on app start, but it may not always be desirable to
run the rest of your data loading steps. See [Run custom commands on containers](#run-custom-commands-on-containers) if you want to run arbitrary commands.

```yaml
version: '2.4'

services:
  dbload:
    container_name: ${APP_NAME}-dbload
    image: ${APP_NAME}:latest
    depends_on:
      - app
    volumes:
      - .:/app
      - ${PWD}/${YOUR_PROJECT}/settings_deployment.py.example:/app/${YOUR_PROJECT}/settings_deployment.py
    # For some reason, Python logs are buffered if they don't come through
    # logging. For instant reporting of non-logging output, i.e., print state-
    # ments or writing to STDOUT directly, run python commands with the -u flag.
    # https://github.com/moby/moby/issues/12447#issuecomment-263846539
    command: >
      bash -c "python manage.py migrate &&
      python -u manage.py import_data &&
      ..."
```

## Using your `docker-compose` setup

### Run the application

If you've defined a `dbload` service, run that first.

```bash
docker-compose -f docker-compose.yml -f docker-compose.db-ops.yml run --rm dbload
```

Then, run your application:

```bash
docker-compose up
```

Meanwhile, run the tests like:

```bash
docker-compose -f docker-compose.yml -f tests/docker-compose.yml run --rm app
```

Stopping your application or test execution is as simple as:

```bash
docker-compose down
```

Prefer `docker-compose down` to manually stopping containers one by one, as it
will stop and clean up all of your containers for you.

### Docker and `pdb`

Say you put a pdb breakpoint in your code to debug a problem. Provided you
included the `stdin_open` and `tty` directives from the standard setup, you
can shell into your container to access your debugger frame like this:

```bash
docker attach ${container_name}
```

`Ctrl-c` to detach when you're finished.

### Run custom commands on containers

Sometimes, you'll want to run an individual command on your container, e.g.,
`update_index` or some data loading operation. Other times, you'll want to run
your application or tests such that you can drop into a pdb shell.

Luckily, that's easy with `docker-compose run`. Simply run a command that looks like
this:

```bash
# The --rm flag will remove the temporary container created to run your command after the command exits.
docker-compose run --rm ${CONTAINER_NAME} ${COMMAND}
```

E.g., to run a specific test module:


```bash
docker-compose -f docker-compose.yml -f tests/docker-compose.yml run --rm app ${YOUR_COMMAND}
```

– where `${YOUR_COMMAND}` is something like `pytest tests/test_admin.py -sxv --pdb`.

Commands that write to STDOUT, e.g., `python manage.py dumpdata`, can be piped (`|`)
or redirected (`>`) to files on your computer in the normal way.

### Install a local installation of a Python package for development

You can use containers to hack on Python packages, too! At DataMade, this comes
up frequently when working on Councilmatic instances that require upstream
changes to [`django-councilmatic`](https://github.com/datamade/django-councilmatic/),
as well as writing or extending [custom comparators](https://github.com/dedupeio/?q=variable)
for Dedupe.io. It's also super helpful for debugging third-party packages.

To install a local copy of a Python package in your Django or Flask application
container, first mount the directory it lives in as a volume.

**`docker-compose.yml`**

```yaml
app:
    container_name: ${CONTAINER}
    image: ${IMAGE}:latest
    volumes:
      - /absolute/path/to/your/local/package:/path/to/package/in/container
    command: ${COMMAND}
```

Next, start your services:


```bash
docker-compose up
```

With your container running, install the package you mounted into your container
as an [editable depedency](https://pip.pypa.io/en/stable/reference/pip_install/#install-editable):

```bash
docker-compose exec app pip install -e /path/to/package/in/container
```

Finally, restart the service you installed the local dependency into so Python
packages are reloaded:

```bash
docker-compose restart app
```

Now, when you make changes to your local installation of the package, they
will automatically be reflected in your application!

#### If installing the dependency directly breaks your application...

If you install a local dependency directly with `pip`, and it breaks the app,
the order of your application dependencies is probably meaningful, and
installing your local depedency out of order interfered with a dependency of
another one of your depndencies. (You begin to understand why the phrase
"dependency hell" exists!)

Luckily, it's negligible to fix in this instance. First, spin down your
containers:

```bash
docker-compose down
```

Then, replace the relevant line in `requirements.txt` with `-e /path/to/package/in/container`.

**`requirements.txt`**

```
# package==0.0.0
-e /path/to/package/in/container
```

Start your services and install all of the dependencies:

```bash
docker-compose up
docker-compose exec app pip install -r requirements.txt
```

Finally, restart the service you installed the local dependency into:

```bash
docker-compose restart app
```

## Debugging your containerized setup

As you extend this pattern, or use new images, you will occasionally find that
things don't quite work as expected. A good base knowledge of the life cycle
of your development environment, plus a few reset strategies, will be good
debugging tools.

### Container life cycle

#### Images

[By definition](https://docs.docker.com/compose/reference/up/), `docker-compose up`
"builds, (re)creates, starts, and attaches to containers for a service." More
precisely, it builds any images _that it can't find on the host_, then proceeds
with the rest.

Your application image is built the first time you run `docker-compose up`. **If
you make subsequent changes to your Dockerfile or development environment, e.g.,
by adding an additional application dependency to `requirements.txt`, you must
rebuild your image using `docker-compose up --build` for the changes to be
reflected in your image.**

#### Containers

`docker-compose up` creates and starts containers for each of the services
defined in `docker-compose.yml`. **In contrast to images, if you change your
service definition, Compose will automatically recreate your application
container.**

If you are attached to a `docker-compose up` command, `Ctrl-C` will stop, but
not remove, your containers.

`docker-compose down` will stop and remove your service containers, as well as
the network that Compose created for them to communicate across.

### Troubleshooting tips

#### Turn it off, then on again

When working with Docker, it's usually best to change one thing at a time, then
test the effects. If you've toggled a lot of switches, or if you want to be
sure you're starting from scratch, you can reset your development environment
like so:

```bash
# Remove your containers and any associated volumes, e.g., your database data
docker-compose down --volumes

# Rebuild and restart your services
docker-compose up --build
```

## A few helpful notes

- Your containerized application should run on the `0.0.0.0` host. In Django,
that looks like `python manage.py runserver 0.0.0.0`.
- The IP addresses for services defined in `docker-compose.yml` are aliased to
the name of the service, e.g., if you need to include a host name for a database
and you are using a containerized version of Postgres defined as a service
called `postgres`, you can use `postgres` as the host name.
- In the case of both the application and the tests, you can access your
containerized database from your computer on the `32001` port, like
`psql -h localhost -p 32001 -U postgres -d ${YOUR_DATABASE}`.
