# Sample Django Cookiecutter

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

The default `babel.config.json` file will transpile JavaScript in your static
directory to syntax that's friendly to modern and legacy browsers but it will
not transpile third-party plug-ins by default.

Some plug-ins target Node versions above ES5, which means that they aren't
compatible for older browsers. Luckily, we can tell Babel to transpile these
dependencies to ensure our apps remain broadly compatible across browsers.

To identify problematic plug-ins, you can use [the `es6-sniffer` CLI](https://github.com/hancush/python-es6-sniffer).

```bash
# Build the es6-sniffer image from GitHub
docker build -t es6-sniffer https://github.com/hancush/python-es6-sniffer.git

# Sniff out potentially incompatible modules
docker run -v sample_sample-node-modules:/node_modules --rm es6-sniffer
```

Once you've found the culprits, add them to the `only` array in
`babel.config.json`. For example:

```json
{
    "only": [
        "./sample/static", // Your JavaScript - default
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
