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
docker build . -t python-cookiecutter:latest
```

### 2. Run `cookiecutter`.

`cd` into your project directory. From here, we'll use `cookiecutter` templates
to generate deployment scripts for your app or server.

From your project directory, run `cookiecutter`:

```bash
docker run -it -v `pwd`:`pwd` -w `pwd` --name cookiecutter python-cookiecutter:latest
```

#### Template variables

When you run `cookiecutter`, it will ask you to define the following variables
in your terminal:

| Variable | Definition |
| - | - |
| `directory_name` | The directory that will contain your generated files. The default, `.`, will put the generated files in your current directory. |
| `app_name` | The slug you use to refer to your application (typically the same as the GitHub repo). |
| `local_settings` | If your project includes a local settings file, set this equal to the relative path to your local settings file (or your example settings file, if it includes working values), and it will be automatically mounted into your application container. Set this to the string `None` if your application does not use a local settings file. |
| `run_command` | The command to run your application. |
| `migrate_command` | The command to migrate your database. |
| `auto_migrate` | Whether your database migration should be run every time you start your application. Set this to False if you have a workflow that involves loading in a database dump. Note that you will need to run migrations manually thereafter, e.g., `docker-compose exec app python manage.py migrate`. |
| `postgis` | Whether to use the Postgis image. |
| `pg_version` | The version of the Postgres or Postgis image you'd like to use. |
| `pg_db` | The name of your database. |


### 3. Customize your configs and scripts.

The templated configs were written to serve our most common use cases.
Sometimes, though, your deployment may require changes or additions to the
boilerplate files.

Perhaps you need to mount additional volumes, or define an extra service, e.g.,
Redis, for queueing.

The world is your oyster! Customize, if/as needed.

### 4. If necessary, initialize your project.

If you're starting a project from scratch, you'll need to define your project
requirements before you start your containerized setup. From your root project
directory, create a requirements file:

```bash
touch requirements.txt
```

At minimum, add Django or Flask to your requirements.

If you're using Django, you can then use your container to generate your project
skeleton.

```bash
docker-compose run --no-deps --rm app django-admin startproject my_project
```

See [the Django docs](https://docs.djangoproject.com/en/2.2/intro/tutorial01/) for more on project setup.


### 5. Run your application!

Run `docker-compose up -d` to build your application and its services, then
go to localhost:8000 (or whatever port you defined in the run command) to view
your containerized app.

See [Using your `docker-compose` setup](../local-development.md#using-your-docker-compose-setup)
for more on local development with Docker.
