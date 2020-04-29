# GitHub Actions

This guide provides documentation for setting up continuous integration with [GitHub Actions](https://help.github.com/en/actions) for different types of projects.

## Contents

- [Running containerized tests](#running-containerized-tests)
- [Deploying a Python package](#deploying-a-python-package)
- [Resources](#resources)

## Running containerized tests

To initialize a workflow for running containerized tests, start by creating a new feature branch in your repo. Then, create a directory called `.github/workflows/` at the root of your repo. GitHub Actions will read any workflows from this directory and run them automatically.

Next, define a file called `main.yml` in the workflows directory, and paste in the following configuration:

```yaml
name: CI

on:
  push:
    branches:
    - master
    - deploy
  pull_request:
    branches:
    - master

jobs:
  test:
    name: Run tests
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v1
    - name: Build containers and run tests
      run: docker-compose -f docker-compose.yml -f tests/docker-compose.yml run --rm app
```

Due to the `on` block, this workflow will run the `test` job on all commits to `master` and all commits to pull requests that have been opened against `master`.

Commit this file to your feature branch and open up a pull request. You should be able to confirm that your workflow runs the tests for your pull request.

### Examples

This workflow is in use in the following projects:

- [Minnesota Election Archive](https://github.com/datamade/mn-election-archive) (visible to DataMade developers only)

## Deploying a Python package

GitHub Actions can run arbitrary code, so we can use it to deploy Python packages to PyPI in addition to testing them.

As above, start by making a new feature branch and creating the directory `.github/workflows/` at the root of your repo if it doesn't yet exist. Then, define two workflow files, one for each of the production and test PyPI instances:

#### 📄`.github/workflows/publish-to-pypi.yml`

```yaml
name: Publish to PyPI

on: push

jobs:
  build-and-publish:
    name: Publish to PyPI
    if: startsWith(github.event.ref, 'refs/tags')
    runs-on: ubuntu-18.04
    steps:
    - uses: actions/checkout@master
    - name: Set up Python 3.7
      uses: actions/setup-python@v1
      with:
        python-version: 3.7
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: '__token__'
        TWINE_PASSWORD: ${{ secrets.pypi_token }}
      run: |
        pip install twine wheel
        pip wheel -w dist --no-deps .
        twine upload --skip-existing dist/*
      continue-on-error: true
```

#### 📄`.github/workflows/publish-to-test-pypi.yml`

```yaml
name: Publish to Test PyPI

on:
  push:
    branches:
      - master

jobs:
  build-and-publish:
    name: Publish to Test PyPI
    runs-on: ubuntu-18.04
    steps:
    - uses: actions/checkout@master
    - name: Set up Python 3.7
      uses: actions/setup-python@v1
      with:
        python-version: 3.7
    - name: Publish to Test PyPI
      env:
        TWINE_USERNAME: '__token__'
        TWINE_PASSWORD: ${{ secrets.test_pypi_token }}
      run: |
        pip install twine wheel
        pip wheel -w dist --no-deps .
        twine upload --skip-existing --repository-url https://test.pypi.org/legacy/ dist/*
      continue-on-error: true
```

Taken together, these two workflows will publish any branch merged into `master` to [test PyPI](https://test.pypi.org/) and publish tagged commits to [PyPI](https://pypi.org/). This structure parallels our practice of keeping a staging site consistent with `master` and pushing tagged commits to production. If the active package version has already been deployed to either instance, the workflows will skip the upload to that instance; this means that only commits that bump the package version in `setup.py` will result in a newly deployed package.

Next, follow the instructions for [creating encrypted secrets](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/creating-and-using-encrypted-secrets#creating-encrypted-secrets) and save values for `pypi_token` and `test_pypi_token`.

To test that this configuration works, you can alter the `on.push.branches` array of `publish-to-test-pypi.yml` to include the name of your feature branch, and you can push a test tag to your feature branch. Make sure to undo these two changes once you've confirmed that your configuration can properly deploy to PyPI and the test PyPI instance.

### Examples

Versions of this workflow are in use in the following packages:

- [`django-geomultiplechoice`](https://github.com/datamade/django-geomultiplechoice/)
- [`pytest-flask-sqlalchemy`](https://github.com/jeancochrane/pytest-flask-sqlalchemy) (no deployment to test PyPI, tests different versions of Python)

## Resources

Our workflows for deploying Python packages to PyPI were adapted from the Python guide to [publishing package distribution releases using GitHub Actions](https://packaging.python.org/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows).

For more detailed information on using GitHub Actions, refer to the [documentation](https://help.github.com/en/actions).
