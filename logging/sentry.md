# Sentry

This document describes how to configure your applications to log errors to
[Sentry](https://sentry.io/), DataMade's preferred error logging service.

## Contents

- [Background](#background)
    - [A note on naming](#a-note-on-naming)
- [Logging errors in Django applications](#logging-errors-in-django-applications)
    - [Option 1: Use the Django app template](#option-1-use-the-django-app-template)
    - [Option 2: Enable Sentry manually](#option-2-enable-sentry-manually)
        - [Install the Sentry SDK](#install-the-sentry-sdk)
        - [Thread the DSN into the app environment](#thread-the-dsn-into-the-app-environment)
        - [Initialize `sentry_sdk` in `settings.py`](#initialize-sentrysdk-in-settingspy)
        - [Group 400 errors](#group-400-errors)

## Background

We use [Sentry](https://sentry.io) as a way to log errors that occur in our applications.
Once you're added to the DataMade organization on Sentry, you should be able to create a
project for your application.

Depending on what kind of application you're building, the code setup for Sentry
will be different. See the docs below for setting up specific application types, but
when in doubt, [refer to the Sentry documentation](https://docs.sentry.io/)
to figure out what steps you'll need to take to configure your application.

### A note on naming

We prefer that Sentry applications share the same name as the GitHub
repo for the project in question. For example, the project with the GitHub repo
[`la-metro-dashboard`](https://github.com/datamade/la-metro-dashboard) should also
have the Sentry application name `la-metro-dashboard`.

## Logging errors in Django applications

Logging errors from Django to Sentry is straightforward using the Sentry Django integration.
When you create an application in Sentry it will provide you with a "Data Source Name,"
or "DSN", a secret string that the Sentry SDK can use to push errors to your application.
You'll then need to update your code to initialize the Sentry SDK and make use of
this DSN.

### Option 1: Use the Django app template

If you used the [Django app template](/docker/templates/) to create your app, your
application will already be configured to push errors to Sentry with the Sentry SDK.
Update your Heroku applications to [add a config
var](https://devcenter.heroku.com/articles/config-vars#managing-config-vars)
called `SENTRY_DSN` representing the DSN for your application, and your app will
be ready to push errors to Sentry.

### Option 2: Enable Sentry manually

If you didn't use the Django app template to create your app, you'll have to take
a few extra steps to prep your app to log errors to Sentry. These steps are adapted
from the [official Sentry docs for Django](https://docs.sentry.io/platforms/python/django/).

#### Install the Sentry SDK

Update your app's `requirements.txt` file to install [`sentry-sdk`](https://pypi.org/project/sentry-sdk/).
Remember to run `docker-compose build` after you update `requirements.txt` to make
sure that your container image requirements are up to date.

#### Thread the DSN into the app environment

Your Django app will need access to the Sentry DSN string in order to push errors to the
correct Sentry application. If you're deploying on Heroku, the easiest way to do this
is with environment variables. Update your [Heroku config
vars](https://devcenter.heroku.com/articles/config-vars#managing-config-vars) to
add a new var, `SENTRY_DSN`, representing the DSN string from Sentry.

If you're deploying with the legacy `settings_local.py` deployment method, you
can also set `SENTRY_DSN` as a global variable in this file and then import it
in `settings.py`.

#### Initialize `sentry_sdk` in `settings.py`

Edit your app's `settings.py` config file and add a block to initialize
Sentry when the app starts up. Import the following modules with the rest of your
`settings.py` imports:

```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
```

If your app threads the Sentry DSN into its environment using an environment variable,
check that variable to see whether to configure Sentry:

```python
if os.getenv('SENTRY_DSN'):
    sentry_sdk.init(
        dsn=os.environ['SENTRY_DSN'],
        integrations=[DjangoIntegration()],
    )
```

If your app uses the legacy `settings_local.py` deployment method, you can try to
import `SENTRY_DSN` from the local settings module:

```python
try:
    from .settings_local import SENTRY_DSN
except ImportError:
    pass
else:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
    )
```

#### Group 400 errors

By default, Django will raise an exception any time a user sends a request to your
app with an HTTP `Host` header that does not match a value in `ALLOWED_HOSTS`.
This should never happen if a human user is requesting your app via a valid
web URL, but it can happen frequently if bot scanners are sending requests to your app.
The can cause lots of annoying Sentry notifications because the `Host` value is
often different from bot to bot, and Sentry will create a separate issue for each
`Host`, making it impossible to tell Sentry to ignore the error.

To ignore these errors, write a `before_send` function in a module like `your_app/logging.py`
to check for this particular error and assign it a custom Sentry fingerprint:

```python
def before_send(event, hint):
    """
    Log 400 Bad Request errors with the same custom fingerprint so that we can
    group them and ignore them all together. See:
    https://github.com/getsentry/sentry-python/issues/149#issuecomment-434448781
    """
    log_record = hint.get('log_record')
    if log_record and hasattr(log_record, 'name'):
        if log_record.name == 'django.security.DisallowedHost':
            event['fingerprint'] = ['disallowed-host']
    return event
```

Then, Update your `sentry_sdk` initialization function to add the function as
a Sentry hook:

```diff
    sentry_sdk.init(
        dsn=SENTRY_DSN,
+       before_send=before_send,
        integrations=[DjangoIntegration()]
    )
```

Now, all 400 errors should be grouped under the same issue in Sentry. Proceed to
the Sentry dashboard and ignore these errors as needed.
