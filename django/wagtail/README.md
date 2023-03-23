# Wagtail CMS

This directory contains best practices for working with [Wagtail](https://wagtail.io/),
DataMade's preferred content management system.

## Contents
- [When to use Wagtail](#when-to-use-wagtail)
- [How to use Wagtail](#how-to-use-wagtail)
- [Supporting editors](#supporting-editors)
- [Research](research/)
    - [Comparisons to existing tools](research/comparisons-to-existing-tools.md)
    - [Recommendation of adoption](research/recommendation-of-adoption.md)
- [Resources for learning](#resources-for-learning)
- [Wagtail Cache](#wagtail-cache)

## When to use Wagtail
A content management system such as Wagtail allows users of a site to add, edit, and delete certain content through a friendly interface separate from the project's code. Wagtail should be used for projects where a client would like the ability to modify content directly without DataMade as an intermediary.

## How to use Wagtail
When at all possible, Wagtail setup should happen at the beginning of a project concurrent with Django setup. Development with a CMS in mind is easier and faster than retrofitting a project with a CMS.

Instead of initializing a Django project with `django-admin startproject`, a Wagtail project should be initialized with:

`wagtail start <YOUR PROJECT NAME>`

See more on getting started with Wagtail [here](https://docs.wagtail.io/en/stable/getting_started/index.html).

## Supporting editors
A CMS is only as powerful as it helps its editors to be. Wagtail offers an editor's guide [here](https://docs.wagtail.io/en/stable/editor_manual/index.html), which can be shared directly with clients.

For any site where people outside DataMade will be using Wagtail, consider creating a non-technical version of the site documentation. For examples that can be used as templates, see:

1. [LISC CDNA](https://docs.google.com/document/d/1H-DKZf71NrwfEoVdnyfvugTu2zGqeIo_fflr0SL3w2c)
2. [Lugar Center Oversight Hearing Index](https://docs.google.com/document/d/1RmmLKMUw2OwjYNAR3Lqh_KfFVYcHDxo9gAJot6tSvKw)

## Resources for learning
- Before beginning a first Wagtail implementation, all developers should read [The Zen of Wagtail](https://docs.wagtail.io/en/v2.8/getting_started/the_zen_of_wagtail.html) to familiarize themselves with the guiding concepts.
- After that, the official [Wagtail documentation](https://docs.wagtail.io/en/stable/) is a good place to start.


## Wagtail Cache
We recommend the `wagtail-cache` library for invalidating the cache whenever a user edits a Wagtail page model. It's simple and lightweight. [Follow the docs to get it setup](https://docs.coderedcorp.com/wagtail-cache/).

Note that wagtail-cache won't invalidate any changes to a custom, non-Wagtail model that is managed in the Wagtail admin dashboard. In that case you'll still need to use the built-in Django caching.

More info about this adoption:
- [how-to issue about this](https://github.com/datamade/how-to/issues/299)
- [PR where we piloted this for the IL NWSS project](https://github.com/datamade/il-nwss-dashboard/pull/157)
- [PR where we used this in for the CRP project](https://github.com/datamade/crp-transparency/pull/134)
