# {{cookiecutter.app_verbose_name}}

## Set-up pre-commit

Pre-commit hooks are scripts that run on your local machine before every commit.

We use the [pre-commit](https://pre-commit.com/) framework to run code linters and formatters that keep our codebase clean.

To set up Pre-Commit, install the Python package on your local machine using

```bash
python -m pip install pre-commit
```

If you'd rather not install pre-commit globally, create and activate a [virtual environment](https://docs.python.org/3/library/venv.html) in this repo before running the above command.

Then, run

```bash
pre-commit install
```

to set up the git hooks.

Since hooks are run locally, you can modify which scripts are run before each commit by modifying `.pre-commit-config.yaml`.

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
a the [github action "publish_docker.yml"](.github/workflows/publish_docker_image.yml). By default, this action is set up to [run when you ask it to manually](https://github.blog/changelog/2020-07-06-github-actions-manual-triggers-with-workflow_dispatch/). You may want to adjust this to run on commits, releases, or pushes to a deployment branch.

After creating an image on a public repo, you probably want to make the package public too. Go to the package settings and change the visibility of the image to public.

![Screenshot 2022-03-23 at 10-54-36 Build software better together](https://user-images.githubusercontent.com/536941/159728240-4590050b-6658-4056-bdfb-4b46eb29d136.png)

If you are on a private repo, [you will need to set up authentication to install an image](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#authenticating-to-the-container-registry).

### Running tests

Run tests with Docker Compose:

```
docker-compose -f docker-compose.yml -f tests/docker-compose.yml run --rm app
```
