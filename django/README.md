# Django

This directory catalogs our preferred Django extensions for common functionality.
In some cases, it also provides extended documentation for setup and use.

**Our cookiecutter for creating a new Django app lives in the [containerization templates](https://github.com/datamade/how-to/tree/master/docker/templates) directory.**

## Standard toolkit

| Objective | Library | Internal documentation |
| :- | :- | :- |
| General wayfinding | [Classy Class-based Views](https://ccbv.co.uk/) | |
| Debugging | [`django-debug-toolbar`](https://github.com/jazzband/django-debug-toolbar) + [`django-debug-toolbar-request-history`](https://github.com/djsutho/django-debug-toolbar-request-history) | |
| CMS | [`wagtail`](https://wagtail.io/developers/) | [Link](wagtail/README.md) |
| Search | [`django-haystack`](https://github.com/django-haystack/django-haystack) | |
| Autocomplete | [`django-autocomplete-light`](https://github.com/yourlabs/django-autocomplete-light) | |
| Cross-browser ES6 support | [`django-compressor`](https://github.com/django-compressor/django-compressor) | [Link](django-compressor.md) |
| API | [`django-rest-framework`](https://github.com/encode/django-rest-framework) + [`django-cors-headers`](https://github.com/ottoyiu/django-cors-headers) | [Link](django-rest-framework.md) |
| File uploads | [`django-storages`](https://django-storages.readthedocs.io/en/latest/) | [Link](file-uploads.md) |
| React integration | [`django-compressor`](https://github.com/django-compressor/django-compressor) | [Link](django-react-integration.md) |
| Translation | [`django-rosetta`](https://django-rosetta.readthedocs.io/) | [Link](translation.md) |
