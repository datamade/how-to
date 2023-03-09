# 🍪 Project template

This directory contains a [cookiecutter](https://github.com/audreyr/cookiecutter)
for DataMade applications.

## Getting started

tk tk tk

Concatenated:

- README
- requirements.txt
- Django settings files

All other files are overridden by Wagtail/React, if included.

#### Template variables

When you run `cookiecutter`, it will ask you to define some or all of the following variables
in your terminal:

| Variable | Definition |
| - | - |
| | |

## Pin your dependencies

For Django apps produced with the `new-django-app` template, you'll always want to at least
pin the requirements in `requirements.txt` and `package.json` to the latest available versions.
We recommend [`pip chill`](https://github.com/rbanffy/pip-chill) and `package-lock.json`
for the task:

```bash
# Run this on your host machine to spawn a shell in an app container
$ docker-compose run --rm app bash

# Run this inside the spawned app container
~ pip-chill | grep -v pip-chill > requirements.txt
~ npm install
```

## Customize your configs and scripts.

The templated configs were written to serve our most common use cases.
Sometimes, though, your deployment may require changes or additions to the
boilerplate files. Perhaps you need to mount additional volumes in your Docker
config, or define an extra service, e.g., Redis for queueing or Elasticsearch for search.

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
a Lead Developer or Partner. Chances are we've made that customization before and can
refer you to an example project.

### 5. Run your application!

Change to your application directory, run `docker-compose up` to build your
application and its services, then go to localhost:8000 (or whatever port you defined
in the run command) to view your containerized app.

See [Using your `docker-compose` setup](https://github.com/datamade/how-to/blob/main/docker/local-development.md)
for more on local development with Docker.
