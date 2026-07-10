# django-compressor

`django-compressor` is a library that provides Django utilities for compressing
linked and inline JavaScript/CSS into a single cached file. At DataMade, we find
it particularly useful for compiling ES6 and React to vanilla JavaScript that can
run on a wide variety of browsers.

Follow the steps below to set up `django-compressor` in your existing Django
project, or use our [`new-django-app` Cookiecutter template](/docker/templates/)
to create a new Django app with `django-compressor` already installed and configured
for you.

## Install Node packages

Using `yarn add`, Update your `package.json` file to include
the following list of Node packages:

- `@babel/cli`
- `@babel/core`
- `@babel/preset-env`
- `@babel/preset-react`
- `babel-preset-env`
- `babelify`
- `browserify`

## Install and configure `django-compressor`

Update your `requirements.txt` file to install `django-compressor`. Then, set the
following settings in `settings.py` to instruct it to bundle your React components:

```python
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_PRECOMPILERS = (
    ('module', 'npx browserify {infile} -t [ babelify --presets [ @babel/preset-env ] ] > {outfile}'),
    ('text/jsx', 'npx browserify {infile} -t [ babelify --presets [ @babel/preset-env @babel/preset-react ] ] > {outfile}'),
)

COMPRESS_OUTPUT_DIR = 'compressor'
```

## Set up caching

The commands that bundle React components can take 2-3 seconds to complete, so
make sure to set up [database caching](https://docs.djangoproject.com/en/3.0/topics/cache/#database-caching)
and [cache your views that use React](https://docs.djangoproject.com/en/3.0/topics/cache/#the-per-view-cache)
to make sure your pages load as quickly as possible.

For an additional level of caching, you might also consider setting up
[offline compression](https://django-compressor.readthedocs.io/en/stable/scenarios/#offline-compression)
in `django-compressor`.

## Use `django-compressor` in your templates

For detailed examples on how to use `django-compressor` to compress and compile your
JavaScript and CSS, see [the `django-compressor`
documentation](https://django-compressor.readthedocs.io/en/stable/usage/).

Note that `<script>` tags with a `type` value of `module` will be compiled as ES6
code, while tags with a `type` value of `text/jsx` will be compiled as React code.

## Further resources

For an example of an app using `django-compressor` in production, see
[BGA Pensions](https://github.com/datamade/bga-pensions/pull/1).
