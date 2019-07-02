# Docker for Local Development

Docker for local development was piloted on `dedupe-service`, a repository to
which some DataMade employees do not have access. Luckily, we can abstract general
patterns for Dockerizing an application to guide our next effort.

## Overview

A containerized local development environment has four components:

1. [A Dockerfile](#dockerfile), containing building instructions for the application itself.
2. [A database initialization script](#scriptsinit-dbsh)
that creates your database and installs any extensions
2. [A root `docker-compose.yml` file](#docker-composeyml)
that declares the application and its dependent services
3. [A `tests/docker-compose.yml` file](#testsdocker-composeyml)
that overrides the application service in the root file, in order to run the tests

### 1. `Dockerfile`

```Dockerfile
# Extend the base Python image
# See https://hub.docker.com/_/python for version options
# N.b., there are many options for Python images. We used the plain
# version number in the pilot. YMMV. See this post for a discussion of
# some options and their pros and cons:
# https://pythonspeed.com/articles/base-image-python-docker-images/
FROM python:<PYTHON_VERSION>

# Give ourselves some credit
LABEL maintainer "DataMade <info@datamade.us>"

# Install and upgrade pip
# This may not be necessary, depending on your base Python image
RUN apt-get update
RUN apt-get install -y python-pip
RUN pip install --upgrade pip setuptools

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

### 2. `scripts/init-db.sh`

The Postgres image provides a harness for executing arbitrary SQL and Bash
scripts when containers are initialized. [Read more. &raquo;](https://docs.docker.com/samples/library/postgres/#initialization-scripts)

```bash
#!/bin/bash
set -e

psql -U postgres -c "CREATE DATABASE <YOUR_DATABASE>"
psql -U postgres -d <YOUR_DATABASE> -c "CREATE EXTENSION IF NOT EXISTS <YOUR_EXTENSION>"
# ad inf.
```

### 3. `docker-compose.yml`

```docker-compose.yml
version: '3'

services:
  app:
    image: <YOUR_APP>
    container_name: <YOUR_APP>
    restart: always
    build: .
    ports:
      # Map ports on your computer to ports on your container. This allows you,
      # e.g., to visit your containerized application in a browser on your
      # computer.
      - <HOST_PORT>:<CONTAINER_PORT>  # e.g., 8000:8000
    depends_on:
      # Declare any services that should be started first. Beware: It checks
      # that a service has started, but not that a service is ready.
      - postgres
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
    container_name: dedupe-postgres
    restart: always
    image: postgres:<YOUR_VERSION>
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

### 4. `tests/docker-compose.yml`

```docker-compose.yml
version: '3'

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
      # docker-compose.yml
      - ...
    command: pytest -sxv
```

### Running the application

Once you've containerized your development environment, run the application
like:

```bash
docker-compose up
```

Meanwhile, run the tests like:

```bash
docker-compose -f docker-compose.yml -f tests/docker-compose.yml run --rm app
# The --rm flag will remove the temporary container created to run your command after the command exits.
docker-compose -f docker-compose.yml -f tests/docker-compose.yml run --rm app <YOUR_COMMAND>
```

– where `<YOUR_COMMAND>` is something like `pytest tests/test_admin.py -sxv --pdb`.

Stop the application or test execution like:

```bash
docker-compose down
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
`psql -h localhost -p 32001 -U postgres -d <YOUR_DATABASE>`.
