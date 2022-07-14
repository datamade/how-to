# GitHub Actions

This guide provides documentation for setting up continuous integration with [GitHub Actions](https://help.github.com/en/actions) for different types of projects.

## Contents

- [Running containerized tests](#running-containerized-tests)
- [Deploying a Python package](#deploying-a-python-package)
- [Deploying a legacy application to CodeDeploy](#deploying-a-legacy-application-to-codedeploy)
- [Setting up Google Lighthouse for accessibility testing](#setting-up-google-lighthouse)
- [Resources](#resources)

## Running containerized tests

N.b., we recommend running containerized tests when the application is containerized in deployment, i.e., deployed to Heroku. For legacy applications deployed on AWS EC2 infrastructure, we recommend a service-based test run. [Skip to deploying a legacy application to CodeDeploy](#deploying-a-legacy-application-to-codedeploy) for an example of this pattern.

To initialize a workflow for running containerized tests, start by creating a new feature branch in your repo. Then, create a directory called `.github/workflows/` at the root of your repo. GitHub Actions will read any workflows from this directory and run them automatically.

Next, define a file called `main.yml` in the workflows directory, and paste in the following configuration:

```yaml
name: CI

on:
  push:
    branches:
    - main
    - deploy
  pull_request:
    branches:
    - main

jobs:
  test:
    name: Run tests
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v1
    - name: Build containers and run tests
      run: docker-compose -f docker-compose.yml -f tests/docker-compose.yml run --rm app
```

Due to the `on` block, this workflow will run the `test` job on all commits to `main` and all commits to pull requests that have been opened against `main`.

If your tests need any additional configurations, such as a `.env` file or a local settings file, add a step to your `test` job to create or copy the necessary files, prior to running the tests. For example:

```yaml
jobs:
  test:
    name: Run tests
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v1
    - shell: bash
      run: |
        cp .env.example .env
    - name: Build containers and run tests
      run: docker-compose -f docker-compose.yml -f tests/docker-compose.yml run --rm app
```

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
    - uses: actions/checkout@main
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
      - main

jobs:
  build-and-publish:
    name: Publish to Test PyPI
    runs-on: ubuntu-18.04
    steps:
    - uses: actions/checkout@main
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

Taken together, these two workflows will publish any branch merged into `main` to [test PyPI](https://test.pypi.org/) and publish tagged commits to [PyPI](https://pypi.org/). This structure parallels our practice of keeping a staging site consistent with `main` and pushing tagged commits to production. If the active package version has already been deployed to either instance, the workflows will skip the upload to that instance; this means that only commits that bump the package version in `setup.py` will result in a newly deployed package.

Next, follow the instructions for [creating encrypted secrets](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/creating-and-using-encrypted-secrets#creating-encrypted-secrets) and save values for `pypi_token` and `test_pypi_token`.

To test that this configuration works, you can alter the `on.push.branches` array of `publish-to-test-pypi.yml` to include the name of your feature branch, and you can push a test tag to your feature branch. Make sure to undo these two changes once you've confirmed that your configuration can properly deploy to PyPI and the test PyPI instance.

### Examples

Versions of this workflow are in use in the following packages:

- [`django-geomultiplechoice`](https://github.com/datamade/django-geomultiplechoice/)
- [`pytest-flask-sqlalchemy`](https://github.com/jeancochrane/pytest-flask-sqlalchemy) (no deployment to test PyPI, tests different versions of Python)

## Deploying a legacy application to CodeDeploy

As above, start by making a new feature branch and creating the directory `.github/workflows/` at the root of your repo if it doesn't yet exist. Then, define a workflow file:

#### 📄`.github/workflows/main.yml`

```yaml
name: CI

on:
  push:
    branches:
      - main
      - deploy
  pull_request:
    branches:
      - main

jobs:
  test:
    name: Run tests
    # 🚨 Update the Ubuntu version to match the server you're deploying to. See
    # https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#jobsjob_idruns-on
    # for supported versions.
    runs-on: ubuntu-${UBUNTU_VERSION}
    services:
      # 🚨 Update the Postgres version and database name to match your app environment and test config
      postgres:
        image: postgres:${POSTGRES_VERSION}
        env:
          POSTGRES_DB: ${POSTGRES_DATABASE}
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    steps:
    - uses: actions/checkout@v2
    # 🚨 Update the Python version to match your app environment
    - name: Set up Python ${PYTHON_VERSION}
      uses: actions/setup-python@v2
      with:
        # Semantic version range syntax or exact version of a Python version
        python-version: '${PYTHON_VERSION}'
    - name: Install dependencies
      run: |
        # 🚨 Need PostGIS? Uncomment these lines to install GDAL.
        # sudo apt update
        # sudo apt install -y gdal-bin
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Test with pytest
      # 🚨 Swap in the correct filenames for your test and application configs
      run: |
        mv ${TEST_CONFIG} ${APP_CONFIG}
        pytest -sv
  deploy:
    needs: test
    name: Deploy to AWS
    runs-on: ubuntu-latest
    steps:
      - uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      - uses: actions/checkout@v2
      - id: deploy
        uses: webfactory/create-aws-codedeploy-deployment@0.2.2
        with:
          # 🚨 Swap in your CodeDeploy application name, which is usually the same as the repository name
          application: ${CODEDEPLOY_APPLICATION_NAME}
```

Update the values indicated inline with the 🚨 emoji. Then, append the following to `.appspec.yml`.

#### 📄`.appspec.yml`

```yaml
# ... deployment lifecycle config ...
branch_config:
  main:
    deploymentGroupName: staging
  deploy:
    deploymentGroupName: production
```

This workflow runs your tests, then creates a deployment conditional on your tests passing. The `deploy` action determines which deployment group, if any, it should create a deployment for using the `branch_config` you added to `.appspec.yml`. In effect, commits to `main` are deployed to staging and commits to `deploy` are deployed to production; commits to all other branches result in a no-op.

Next, follow the instructions for [creating encrypted secrets](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/creating-and-using-encrypted-secrets#creating-encrypted-secrets) and save values for `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`, using the developer credentials in our team LastPass.

To test that this configuration works, you can update the `on.push.branches` array of `main.yml` to include the name of your feature branch, and point your branch to the staging deployment group in the `branch_config` block of `.appspec.yml`. The result should be a staging deployment of your app on the next commit to your branch. Don't forget to revert these changes once you've tested the integration.

### Examples

This workflow is in use in the following applications:

- [`la-metro-councilmatic`](https://github.com/datamade/la-metro-councilmatic)
- [`la-metro-dashboard`](https://github.com/datamade/la-metro-dashboard)

## Setting Up Google Lighthouse
Google Lighthouse is a tool that provides information on 5 different areas of performance for websites. We only use it to run accessibility audits on our sites prior to deploying to production, and using Lighthouse is the first step in the Accessibility section of our [site launch checklist](https://github.com/datamade/site-launch-checklist).

The documentation for Google's Lighthouse can be found [here](https://github.com/GoogleChrome/lighthouse-ci/blob/main/docs/getting-started.md), along with some basic configuration. Since we only use Lighthouse for accessibility audits, our configuration files are set up a bit differently.

1. List the audits you would like to run in a file named `lighthouserc.js` in the root of the application directory:

```js
module.exports = {
  ci: {
    collect: {
        staticDistDir: './cms_app/templates/',
      },
      assert: {
        preset: 'lighthouse:recommended',
        assertions: {
          'categories:accessibility': ['error', {'minScore': 0.9}],
          'apple-touch-icon': 'off',
          'content-width': 'off',
          'csp-xss': 'off',
          'doctype': 'off',
          'document-title': 'off',
          'errors-in-console': 'off',
          'font-size': 'off',
          'heading-order': 'off',
          'html-has-lang': 'off',
          'installable-manifest': 'off',
          'interactive': 'off',
          'is-on-https': 'off',
          'legacy-javascript': 'off',
          'maskable-icon': 'off',
          'meta-description': 'off',
          'no-vulnerable-libraries': 'off',
          'render-blocking-resources': 'off',
          'service-worker': 'off',
          'splash-screen': 'off',
          'tap-targets': 'off',
          'themed-omnibox': 'off',
          'unminified-javascript': 'off',
          'unused-javascript': 'off',
          'uses-long-cache-ttl': 'off',
          'viewport': 'off',
        },
      },
    upload: {
      target: 'temporary-public-storage',
    },
  },
};
```

2. Configure GitHub Actions in `.github/workflows/main.yml`
```yaml
...
jobs:
  lhci:
    name: Lighthouse
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Use Node.js 12.x
        uses: actions/setup-node@v1
        with:
          node-version: 12.x
      - name: run Lighthouse CI
        run: |
          npm install -g @lhci/cli@0.8.x
          lhci autorun
...
```

See [Running Containerized Tests](#running-containerized-tests) for what additional features of a `.github/workflows/main.yml` file.

For an example of Lighthouse built into a CI pipeline, see the [`lighthouse-ci` branch of the CPS app](https://github.com/datamade/cps-ssce-dashboard/tree/lighthouse-ci).

## Resources

Our workflows for deploying Python packages to PyPI were adapted from the Python guide to [publishing package distribution releases using GitHub Actions](https://packaging.python.org/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows).

Our workflow for deploying to CodeDeploy via GitHub Actions comes from [Webfactory's `create-aws-codedeploy-deployment` action](https://github.com/marketplace/actions/webfactory-create-aws-codedeploy-deployment), which includes further details on configuration and usage.

For more detailed information on using GitHub Actions, refer to the [documentation](https://help.github.com/en/actions).
