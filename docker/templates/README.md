# 🍪 Containerization templates

This directory contains [cookiecutters](https://github.com/audreyr/cookiecutter)
for the containerization of web applications.

## Getting started

### 1. Set up.

Install `cookiecutter` in your virtual environment of choice. (It's a [great
candidate for `gus`](https://github.com/datamade/ops/wiki/How-to-DataMade-(Resources-for-new-hires)#python)!)

```bash
pip install cookiecutter
```

Then, clone this repository to your favorite working directory –

```bash
git clone https://github.com/datamade/how-to.git
```

– or update your local version.

```bash
cd /path/to/how-to
git pull
```

### 2. Run `cookiecutter`.

`cd` into your project directory. From here, we'll use `cookiecutter` templates
to generate deployment scripts for your app or server.

From your project directory, run `cookiecutter`:

```bash
cookiecutter how-to/docker/templates/python
```

#### Template variables

When you run `cookiecutter`, it will ask you to define the following variables
in your terminal:

| Variable | Definition |
| - | - |
| `directory_name` | The directory that will contain your generated files. We'll move the files out and remove this directory after running `cookiecutter` so it's fine to use the default here. |
| `app_name` | The name of your application. |
| `local_settings` | If your project includes a local settings file, set this equal to the relative path to your local settings file (or your example settings file, if it includes working values), and it will be automatically mounted into your application container. Set this to None if your application does not use a local settings file. |
| `run_command` | The command to run your application. |
| `migrate_command` | The command to migrate your database. |
| `auto_migrate` | Whether your database migration should be run every time you start your application. Set this to False if you have a workflow that involves loading in a database dump. Note that you will need to run migrations manually thereafter, e.g., `docker-compose exec app python manage.py migrate`. |
| `postgis` | Whether to use the Postgis image. |
| `pg_version` | The version of the Postgres or Postgis image you'd like to use. |
| `pg_db` | The name of your database. |

### 3. Relocate the generated files.

Unless you specified another value for `directory_name` when you ran
`cookiecutter`, the generated files will land in a directory called
`python-template`.

Copy the generated files to your top-level project directory, then remove the
generated directory. (Note that this will preserve `configs/` and `scripts/`
directories and their contents, if your project already contains them.)

```bash
# Replace <directory_name> with the appropriate value!
rsync -av <directory_name>/* . && rm -rf <directory_name>/
```

### 4. Customize your configs and scripts.

The templated scripts and configs were written to serve our most common use
cases. Sometimes, though, your deployment may require changes or additions to
the boilerplate files.

The world is your oyster! Customize your scripts, if/as needed.
