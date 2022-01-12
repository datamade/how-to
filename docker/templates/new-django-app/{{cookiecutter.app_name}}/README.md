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

### Github Docker Images
You can build docker images and deploy them to github's container registry using
a the [github action "publish_docker.yml"](.github/workflows/publish_docker_image.yml). By default, this action is set up to [run when you ask it too manually](https://github.blog/changelog/2020-07-06-github-actions-manual-triggers-with-workflow_dispatch/). You may want to adjust this to run on commits, releases, or pushes to a deployment branch.

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
docker run -v {{ cookiecutter.app_name }}_{{ cookiecutter.app_name }}-node-modules:/node_modules --rm es6-sniffer
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
