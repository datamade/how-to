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

## Components

### 1. `Dockerfile`

```Dockerfile
# Extend the base Python image
# See https://hub.docker.com/_/python for version options
# N.b., there are many options for Python images. We used the plain
# version number in the pilot. YMMV. See this post for a discussion of
# some options and their pros and cons:
# https://pythonspeed.com/articles/base-image-python-docker-images/
FROM python:3.7

# Give ourselves some credit
LABEL maintainer "DataMade <info@datamade.us>"

# Install any additional OS-level packages you need via apt-get. RUN statements
# add additional layers to your image, increasing its final size. Keep your
# image small by combining related commands into one RUN statement, e.g.,
#
# RUN apt-get update && \
#     apt-get install -y python-pip
#
# Read more on Dockerfile best practices at the source:
# https://docs.docker.com/develop/develop-images/dockerfile_best-practices

# Inside the container, create an app directory and switch into it
RUN mkdir /app
WORKDIR /app

# Copy the requirements file into the app directory, and install them. Copy
# only the requirements file, so Docker can cache this build step. Otherwise,
# the requirements must be reinstalled every time you build the image after
# the app code changes. See this post for further discussion of strategies
# for building lean and efficient containers:
# https://blog.realkinetic.com/building-minimal-docker-containers-for-python-applications-37d0272c52f3
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the contents of the current host directory (i.e., our app code) into
# the container.
COPY . /app
```

### 2. `docker-compose.yml`

There are [several versions](https://docs.docker.com/compose/compose-file/compose-versioning/)
of `docker-compose` syntax. We prefer v2, in order to take advantage of health
checks and expressive `depends_on` declarations. This allows us to delay the
start of an application until the services it needs have finished building.

v3 no longer supports this syntax. More on that [in this issue](https://github.com/peter-evans/docker-compose-healthcheck/issues/3#issuecomment-329037485).

```yaml
version: '2.4'

services:
  app:
    image: <YOUR_APP>
    container_name: <YOUR_APP>
    restart: always
    build: .
    # Allow container to be attached to, e.g., to access the pdb shell
    stdin_open: true
    tty: true
    ports:
      # Map ports on your computer to ports on your container. This allows you,
      # e.g., to visit your containerized application in a browser on your
      # computer.
      - <HOST_PORT>:<CONTAINER_PORT>  # e.g., 8000:8000
    depends_on:
      postgres:
        condition: service_healthy
    volumes:
      # Mount the development directory as a volume into the container, so
      # Docker automatically recognizes your changes.
      - .:/app
      # Mount example configs as live configs in the container.
      - ${PWD}/<YOUR_PROJECT>/settings_deployment.py.example:/app/<YOUR_PROJECT>/settings_deployment.py
    command: <RUNSERVER_COMMAND>  # e.g., python manage.py runserver 0.0.0.0:8000

  migration:
    container_name: <YOUR_APP>-migration
    image: <YOUR_APP>:latest
    depends_on:
      # Declaring this dependency ensures that your application image is built
      # before migrations are run, and that your application and migrations can
      # be run from the same image, rather than creating purpose-specific
      # copies.
      - app
    volumes:
      # These should generally be the same as your application volumes.
      - .:/app
      - ${PWD}/<YOUR_PROJECT>/settings_deployment.py.example:/app/<YOUR_PROJECT>/settings_deployment.py
    command: <MIGRATION_COMMAND>  # e.g., python manage.py migrate

  postgres:
    container_name: <YOUR_APP>-postgres
    restart: always
    image: postgres:11
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    environment:
      # The default Postgres image exposes a number of environmental variables
      # that allow you to configure the container's behavior, without writing
      # any additional code. Specify the name of your database, and any other
      # variables, here. https://hub.docker.com/_/postgres/#environment-variables
      POSTGRES_DB: <YOUR_DB>
    volumes:
      # By default, Postgres instantiates an anonymous volume. Use a named
      # one, so your data persists beyond the life of the container. See this
      # post for a discussion of the pitfalls of Postgres and anonymous
      # volumes: https://linuxhint.com/run_postgresql_docker_compose/
      - <YOUR_APP>-db-data:/var/lib/postgresql/data
      # Mount our initialization script.
      - ${PWD}/scripts/init-db.sh:/docker-entrypoint-initdb.d/10-init.sh
    ports:
      - 32001:5432

volumes:
  # Declare your named volume for Postgres.
  <YOUR_APP>-db-data:
```

### 3. `tests/docker-compose.yml`

```yaml
version: '2.4'

services:
  app:
    # Don't restart the service when the command exits
    restart: "no"
    environment:
      # Define any relevant environmental variables here
      - ...
    volumes:
      # Multi-value fields are concatenated, i.e., this file will be mounted
      # in addition to the files and directories specified in the root
      # docker-compose.yml, so we don't need to specify those volumes again
      - ...
    command: pytest -sxv
```

### 4. `scripts/init-db.sh` (Optional)

The default Postgres image exposes [a number of environmental variables](https://hub.docker.com/_/postgres/#environment-variables)
that allow you to define custom behavior for your container without writing
additional code. Things you can achieve via environmental variables include
creating your default database, specifying a default user and password, and
customizing the location of the database files.

If you need more advanced functionality, e.g., installing a custom Postgres
extension, the Postgres image provides a harness for executing arbitrary SQL
and Bash scripts when a container is initialized. [Read more. &raquo;](https://docs.docker.com/samples/library/postgres/#initialization-scripts)

***If you would like to use the Postgis extension,*** we recommend using a
Postgis image, rather than configuring it in an initialization script. Rec tk.

```bash
#!/bin/bash
set -e

psql -U postgres -c "CREATE DATABASE <YOUR_DATABASE>"
psql -U postgres -d <YOUR_DATABASE> -c "CREATE EXTENSION IF NOT EXISTS <YOUR_EXTENSION>"
# Add any more database initialization commands you may need here
```

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
