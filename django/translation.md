# Translating Django apps

This document describes our best practices for translating Django apps.

The Django documentation for translation (or, in technical terms,
[internationalization and localization](https://docs.djangoproject.com/en/3.0/topics/i18n/))
is quite extensive and we encourage you to read it if you plan to translate a
Django app. This document will not explain in detail how translation works in
Django, so think of it as a supplement to the official docs.

## Contents

- [Internationalization](#internationalization)
    - [Configure Django settings for translations](#configure-django-settings-for-translations)
    - [Tag strings for translation](#tag-strings-for-translation)
- [Localization](#localization)
    - [Install Rosetta](#install-rosetta)
    - [Make message files](#make-message-files)
    - [Keep message files under version control](#keep-message-files-under-version-control)
    - [Compile messages on build and deploy](#compile-messages-on-build-and-deploy)
    - [Automatically reload catalog files during translation](#automatically-reload-catalog-files-during-translation)
- [Exmaples](#examples)

## Internationalization

Internationalization refers to the process of setting up an application for
translation into multiple langauges. Internationalization is typically performed
by the developers of an app as a separate step from the translation itself.

### Configure Django settings for translations

Configure the following settings to initialize translation support. Note that you can
change these settings later if your translation needs change.

- `LANGUAGES`: This variable should be set to a tuple of tuples representing all
  the languages you want to support in your app. For an example, see
  [the docs](https://docs.djangoproject.com/en/3.0/ref/settings/#languages).

- `LOCALE_PATHS`: Set this to a subdirectory of your app like `locale` to instruct
  Django to store translation files there. For example:

```python
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
```

- Set the following additional settings to enable translations and timezone support:

```python
# Translations
LANGUAGE_CODE = 'en'
USE_I18N = True
USE_L10N = True

# Time zones
TIME_ZONE = 'UTC'
USE_TZ = True
```

### Tag strings for translation

Django provides detailed documentation of their API for tagging strings for
translation in different parts of an app, including in views, models, templates,
and URL patterns. [Read these docs](https://docs.djangoproject.com/en/3.0/topics/i18n/translation/)
to learn how to tag strings for translation.

## Localization

Localization refers to the process of translating tagged strings for display
to the end user. Localization is typically performed by a team of external
translators using config files and interfaces supplied by app developers.

### Install Rosetta

[`django-rosetta`](https://django-rosetta.readthedocs.io/) is a Django app that
provides a friendly admin interface for translators. Follow the
[setup instructions](https://django-rosetta.readthedocs.io/installation.html)
to install it in your app.

### Make message files

In order to expose your translation strings to translators, you can use Django's
`makemessages` command to search your app for translation strings and collect them in
message files (or `.po` files) for translation. The cleanest way to do this is to run it
locally and save the resulting `.po` files to version control:

```
docker-compose run --rm app ./manage.py makemessages --all
git add locale/*/LC_MESSAGES/*.po
```

### Keep message files under version control

One of the key conceptual challenges of using an interface like Rosetta for
localization is that updated `.po` files are stored on the server, which
may cause them to get out of sync with version control. This is particularly
problematic for apps with ephemeral filesystems, like those deployed on Heroku.

To get around this problem, we recommend that you work with translators to
download updated `.po` files from the server and save them to version control.
On Heroku, you can do this with the
[`heroku ps:copy` command](https://devcenter.heroku.com/articles/heroku-cli-commands#heroku-ps-copy-file).

### Compile messages on build and deploy

Since compiled `.mo` files are not human-readable and are fully derived from `.po` files,
we recommend you **not** keep them under version control and instead compile
them dynamically.

Instead of keeping `.mo` files under version control, update your `Dockerfile`
and `release.sh` script to compile them dynamically using the following command
whenever the app is built or deployed:

```
python manage.py compilemessages
```

### Automatically reload catalog files during translation

While translators are working, make sure to set the `ROSETTA_WSGI_AUTO_RELOAD`
environment variable to `True` for your deployed application. This will cause the gettext
catalog files to automatically reload every time they are modified. For performance
reasons, make sure to unset this variable in production environments and once
translation is finished.

## Examples

- [WhoWasInCommand](https://github.com/security-force-monitor/sfm-cms/) is
  translated in more than three languages and uses Rosetta for localization.
