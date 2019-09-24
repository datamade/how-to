# Deploy a Django app to Heroku

This guide provides instructions on deploying a Django app to Heroku, DataMade's
preferred platform for hosting dynamic applications.

## Contents

- [Set up application code for Heroku](#set-up-application-code-for-heroku)
    - [Containerize your app](#containerize-your-app)
    - [Serve static files with WhiteNoise](#serve-static-files-with-whitenoise)
    - [Read settings and secret variables from the environment](#read-settings-and-secret-variables-from-the-environment)
- [Provision Heroku resources](#provision-heroku-resources)
    - [Ensure that the Heroku CLI is installed](#ensure-that-the-heroku-cli-is-installed)
    - [Create Heroku config files](#create-heroku-config-files)
        - [`heroku.yml`](#heroku.yml)
        - [`release.sh`](#release.sh)
        - [`app.json`](#app.json)
    - [Create apps and pipelines for your project](#create-apps-and-pipelines-for-your-project)
- [Troubleshooting](#troubleshooting)

## Set up application code for Heroku

In order to deploy a Django application to Heroku, a few specific configurations
need to be enabled in your application code. We provide details on these
configurations below.

### Containerize your app

We use Heroku as a platform for deploying containerized apps, which means that
your app must be containerized in order to use Heroku properly. If your app
is not yet containerized, [follow our instructions for containerizing Django
apps](/docker/local-development.md) before moving on.

### Serve static files with WhiteNoise

Apps deployed on Heroku don't typically use Nginx to serve content, so they need some
other way of serving static files. Since our apps tend to have relatively low traffic,
we prefer configuring [WhiteNoise](http://whitenoise.evans.io/)
to allow Django to serve static files in production.

Follow the [setup instructions for WhiteNoise in
Django](http://whitenoise.evans.io/en/stable/django.html) to ensure that your
Django apps can serve static files.

### Read settings and secret variables from the environment

Heroku doesn't allow us to decrypt content with GPG, so we can't use Blackbox
to decrypt application secrets. Instead, we can store these secrets as [config
vars](https://devcenter.heroku.com/articles/config-vars), which Heroku will thread
into our container environment.

The three most basic config vars that you'll want to set for every app include
the Django `DEBUG`, `SECRET_KEY`, and `ALLOWED_HOSTS` variables. Update `settings.py`
to read these variables from the environment:

```python
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
DEBUG = os.getenv('DJANGO_DEBUG', True)	DEBUG = False if os.getenv('DJANGO_DEBUG', True) == 'False' else True
allowed_hosts = os.getenv('DJANGO_ALLOWED_HOSTS', [])
ALLOWED_HOSTS = allowed_hosts.split(',') if allowed_hosts else []
```

Make sure to update your app service in `docker-compose.yml` to thread any variables
that don't have defaults into your local environment:

```yml
services:
  app:
    environment:
      - DJANGO_SECRET_KEY=really-super-secret
```

## Provision Heroku resources

Once your application is properly configured for Heroku, the following instructions
will help you deploy your application to the platform.

### Ensure that the Heroku CLI is installed

The fastest way to get a project up and running on Heroku is to use the
[Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli). Before you start,
make sure you have the CLI installed locally. In addition, confirm that you have the
manifest plugin) installed:

```
heroku plugins | grep manifest
```

If you don't see any output, [follow the official instructions for installing the
plugin](https://devcenter.heroku.com/changelog-items/1441).

### Create Heroku config files

Define config files relative to the root of your repo.

#### `heroku.yml`

The `heroku.yml` manifest file tells Heroku how to build and network the services
and containers that comprise your application. This file should live in the root of your project repo.
For background and syntax, see [the
documentation](https://devcenter.heroku.com/articles/build-docker-images-heroku-yml).
Use the following baseline to get started:

```yml
# Define addons that you need for  your project, such as Postgres, Redis, or Solr.
setup:
  addons:
    - plan: heroku-postgresql
# Define your application's Docker containers.
build:
  docker:
    web: Dockerfile
# Define any scripts that you'd like to run every time the app deploys.
release:
  command:
    - ./scripts/release.sh
  image: web
# The command that runs your application. Replace 'app' with the name of your app.
run:
  web: gunicorn -t 180 --log-level debug app.wsgi:application
```

#### `release.sh`

In your app's `scripts` folder, define a script `release.sh` to run every time the app deploys.
Use the following baseline script:

```bash
#!/bin/bash
python manage.py collectstatic --noinput
python manage.py migrate --noinput
```

#### `app.json`

In order to enable [review apps](https://devcenter.heroku.com/articles/github-integration-review-apps)
for your project, the repo must contain an `app.json` config file in the root directory.
For background and syntax, see [the documentation](https://devcenter.heroku.com/articles/app-json-schema).
Use the following baseline to get started:

```json
{
  "name": "your-app",
  "description": "Short description of your app.",
  "scripts": {},
  "env": {
    "DATABASE_URL": {
      "required": true
    },
    "DJANGO_SECRET_KEY": {
      "required": true
    }
  },
  "formation": {
    "web": {
      "quantity": 1,
      "size": "hobby"
    }
  },
  "addons": [
    "heroku-postgresql"
  ],
  "buildpacks": [],
  "stack": "container"
}
```

### Create apps and pipelines for your project

In order to deploy your project, you need to create Heroku apps for staging
and production, and tie them together in a [pipeline](https://devcenter.heroku.com/articles/pipelines).
To create these resources, start by defining the name of your app:

```bash
# This should be the same slug as your project's GitHub repo.
export APP_NAME=<your-app-name-here>
```

Then, run the following Heroku CLI commands:

```bash
heroku create ${APP_NAME} -t datamade --manifest
heroku pipelines:create -t datamade ${APP_NAME} -a ${APP_NAME} -s production
heroku create ${APP_NAME}-staging -t datamade --manifest
heroku pipelines:add ${APP_NAME}-staging -a ${APP_NAME}-staging -s staging
heroku pipelines:connect ${APP_NAME} -r datamade/${APP_NAME}
heroku reviewapps:enable -a ${APP_NAME}-staging -p ${APP_NAME}
```

Next, configure the GitHub integration to set up [automatic
deploys](https://devcenter.heroku.com/articles/github-integration#automatic-deploys)
for both Heroku apps (staging and production). Choose "Wait for CI to pass before deploy" for each app.

Finally, configure environment variables for both Heroku apps. These can be set
using either the dashboard or the CLI. [Follow the Heroku
documentation](https://devcenter.heroku.com/articles/config-vars#managing-config-vars)
to set up your config vars.

## Troubleshooting

### I see `Application error` or a `Welcome to Heroku` page on my site

If your app isn't loading at all, check the dashboard to make sure that the most
recent build and release cycle passed. If the build and release both passed,
check the `Dyno formation` widget on the app `Overview` page to make sure that
dynos are enabled for your `web` process.

### Debugging Heroku CLI errors

Sometimes a Heroku CLI command will fail without showing much output (e.g. `Build failed`).
In these cases, you can set the following debug flag to show the raw HTTP responses
from the Heroku API:

```bash
export HEROKU_DEBUG=1
```
