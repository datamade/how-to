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

### Ensuring browser compatibility

Some plug-ins target Node versions above ES5, which means that they aren't
compatible for some browsers. Luckily, we can tell Babel to transpile these
dependencies to ensure our apps are broadly compatible across browsers.

To identify problematic plug-ins, you can use [the `es6-sniffer` CLI](https://github.com/hancush/python-es6-sniffer).

```bash
# Build the es6-sniffer image from GitHub
docker build -t es6-sniffer https://github.com/hancush/python-es6-sniffer.git

# Sniff out potentially incompatible modules
docker run --v {{ cookiecutter.app_name }}_{{ cookiecutter.app_name }}-node-modules:/node_modules --rm es6-sniffer
```

Once you've found the culprits, add them to the `only` array in
`babel.config.json`. For example:

```json
{
    "only": [
        "./{{ cookiecutter.module_name }}/static", // Your JavaScript - default
        "./node_modules/problem_module_a",
        "./node_modules/problem_module_b"
    ],
    // The rest of your config
}
```

### Running tests

Run tests with Docker Compose:

```
docker-compose -f docker-compose.yml -f tests/docker-compose.yml run --rm app
```
