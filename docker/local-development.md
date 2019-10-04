# Docker for Local Development

Docker for local development was piloted on `dedupe-service`, a repository to
which some DataMade employees do not have access. Luckily, we have since applied
the pattern to other projects. Some examples in the wild:

- [🏡 `ihs-website-v2`](https://github.com/datamade/ihs-website-v2)
- [🏆 `lisc-cdna`](https://github.com/datamade/lisc-cnda)

## Overview

A containerized local development environment has four components, and one
optional service:

1. [A Dockerfile](#1-dockerfile), containing building instructions for the application itself.
2. [A root `docker-compose.yml` file](#3-docker-composeyml)
that declares the application and its dependent services
3. [A `tests/docker-compose.yml` file](#4-testsdocker-composeyml)
that overrides the application service in the root file, in order to run the tests
4. [A database initialization script](#2-scriptsinit-dbsh-optional)
that creates your database and installs any extensions (Optional)
5. [A `docker-compose.db-ops.yml` file](#5-docker-composedb-opsyml-optional)
that automates a multi-step data loading routine (Optional)

With this setup, you can:

- [Run your application or tests](#run-the-application)
- [Access the `pdb` shell](#docker-and-pdb)
- [Run custom commands on your container](#run-custom-commands-on-containers)

The three primary components of a containerized setup for local development are
templated for reuse in the `templates/` directory. See [the README](templates/README.md)
for instructions for use.

## Components

### 1. `Dockerfile`

📄 [`Dockerfile`](templates/python/{{cookiecutter.directory_name}}/Dockerfile)

### 2. `docker-compose.yml`

📄 [`docker-compose.yml`](templates/python/{{cookiecutter.directory_name}}/docker-compose.yml)

There are [several versions](https://docs.docker.com/compose/compose-file/compose-versioning/)
of `docker-compose` syntax. We prefer v2, in order to take advantage of health
checks and expressive `depends_on` declarations. This allows us to delay the
start of an application until the services it needs have finished building.

v3 no longer supports this syntax. More on that [in this issue](https://github.com/peter-evans/docker-compose-healthcheck/issues/3#issuecomment-329037485).

### 3. `tests/docker-compose.yml`

📄 [`tests/docker-compose.yml`](templates/python/{{cookiecutter.directory_name}}/tests/docker-compose.yml)

### 4. `scripts/init-db.sh` (Optional)

The default Postgres image exposes [a number of environmental variables](https://hub.docker.com/_/postgres/#environment-variables)
that allow you to define custom behavior for your container without writing
additional code. Things you can achieve via environmental variables include
creating your default database, specifying a default user and password, and
customizing the location of the database files.

If you need more advanced functionality, e.g., installing a custom Postgres
extension, the Postgres image provides a harness for executing arbitrary SQL
and Bash scripts when a container is initialized. [Read more. &raquo;](https://docs.docker.com/samples/library/postgres/#initialization-scripts)

```bash
#!/bin/bash
set -e

psql -U postgres -c "CREATE DATABASE <YOUR_DATABASE>"
psql -U postgres -d <YOUR_DATABASE> -c "CREATE EXTENSION IF NOT EXISTS <YOUR_EXTENSION>"
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

### 5. `docker-compose.db-ops.yml` (Optional)

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
    container_name: <APP_NAME>-dbload
    image: <APP_NAME>:latest
    depends_on:
      - app
    volumes:
      - .:/app
      - ${PWD}/<YOUR_PROJECT>/settings_deployment.py.example:/app/<YOUR_PROJECT>/settings_deployment.py
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
docker attach <container_name>
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
docker-compose run --rm <CONTAINER_NAME> <COMMAND>
```

E.g., to run a specific test module:


```bash
docker-compose -f docker-compose.yml -f tests/docker-compose.yml run --rm app <YOUR_COMMAND>
```

– where `<YOUR_COMMAND>` is something like `pytest tests/test_admin.py -sxv --pdb`.

Commands that write to STDOUT, e.g., `python manage.py dumpdata`, can be piped (`|`)
redirected (`>`) to files on your computer in the normal way.

If you need to run a command that writes to files, e.g., `python manage.py makemigrations`,
and you'd like those files to be written to your host machine, you can use this trick:

```bash
docker-compose run --no-deps --rm -v `pwd`:`pwd` -w `pwd` app python manage.py makemigrations -n mymigration
```

`--no-deps` means start the application container, but not any dependent services,
e.g., the database. ``-v `pwd`:`pwd` -w `pwd` `` mounts your working
directory into your container and executes your command inside of it. The
effect is that any files generated by the command are placed in your project
directory on your computer, instead of inside the container.

## A few helpful notes

- Your containerized application should run on the `0.0.0.0` host. In Django,
that looks like `python manage.py runserver 0.0.0.0`.
- The IP addresses for services defined in `docker-compose.yml` are aliased to
the name of the service, e.g., if you need to include a host name for a database
and you are using a containerized version of Postgres defined as a service
called `postgres`, you can use `postgres` as the host name.
- In the case of both the application and the tests, you can access your
containerized database from your computer on the `32001` port, like
`psql -h localhost -p 32001 -U postgres -d <YOUR_DATABASE>`.
