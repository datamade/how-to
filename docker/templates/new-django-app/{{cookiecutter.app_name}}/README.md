# {{cookiecutter.app_verbose_name}}

## Developing

Development requires a local installation of [Docker](https://docs.docker.com/install/)
and [Docker Compose](https://docs.docker.com/compose/install/).

Build application containers:

```
docker-compose build
```

Run the app:

```
docker-compose up
```

The app will be available at http://localhost:8000. The database will be exposed
on port 32001.

### Running tests

Run tests with Docker Compose:

```
docker-compose -f docker-compose.yml -f tests/docker-compose.yml run --rm app
```
