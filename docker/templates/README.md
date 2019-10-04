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
docker run -it --name cookiecutter python-cookiecutter:latest
```

#### Template variables

When you run `cookiecutter`, it will ask you to define the following variables
in your terminal:

| Variable | Definition |
| - | - |
| `directory_name` | The directory that will contain your generated files. We'll move the files out and remove this directory after running `cookiecutter` so it's fine to use the default here. |
| `app_name` | The slug you use to refer to your application (typically the same as the GitHub repo). |
| `local_settings` | If your project includes a local settings file, set this equal to the relative path to your local settings file (or your example settings file, if it includes working values), and it will be automatically mounted into your application container. Set this to None if your application does not use a local settings file. |
| `run_command` | The command to run your application. |
| `migrate_command` | The command to migrate your database. |
| `auto_migrate` | Whether your database migration should be run every time you start your application. Set this to False if you have a workflow that involves loading in a database dump. Note that you will need to run migrations manually thereafter, e.g., `docker-compose exec app python manage.py migrate`. |
| `postgis` | Whether to use the Postgis image. |
| `pg_version` | The version of the Postgres or Postgis image you'd like to use. |
| `pg_db` | The name of your database. |

### 3. Relocate the generated files.

The generated files will land in a directory inside your container called
`python-template`.

Copy the generated files to your top-level project directory, then remove the
container.

```bash
docker cp cookiecutter:/python-template/. .
docker rm cookiecutter
```

### 4. Customize your configs and scripts.

The templated scripts and configs were written to serve our most common use
cases. Sometimes, though, your deployment may require changes or additions to
the boilerplate files.

The world is your oyster! Customize your scripts, if/as needed.
