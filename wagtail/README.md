# Wagtail

This directory contains best practices for working with [Wagtail](https://wagtail.io/),
DataMade's preferred content management system.

## Contents
- [When to use Wagtail](#when-to-use-wagtail)
- [How to use Wagtail](#how-to-use-wagtail)
- [Research](research/)
    - [Comparisons to existing tools](research/comparisons-to-existing-tools.md)
    - [Recommendation of Adoption](research/recommendation-of-adoption.md)
- [Resources for Learning](#resources-for-learning)

## When to use Wagtail
A content management system such as Wagtail allows users of a site to add, edit, and delete certain content through a friendly interface separate from the project's code. Wagtail should be used for projects where a client would like the ability to modify content directly without DataMade as an intermediary.

## How to use Wagtail
When at all possible, Wagtail setup should happen at the beginning of a project concurrent with Django setup. Development with a CMS in mind is easier and faster than retrofitting a project with a CMS.

Instead of initializing a Django project with `django-admin startproject`, a Wagtail project should be initialized with:

`wagtail start <YOUR PROJECT NAME>`

See more on getting started with Wagtail [here](https://docs.wagtail.io/en/stable/getting_started/index.html).

## Resources for Learning
- Before beginning a first Wagtail implementation, all developers should read [The Zen of Wagtail](https://docs.wagtail.io/en/v2.8/getting_started/the_zen_of_wagtail.html) to familiarize themselves with the guiding concepts.
- After that, the official [Wagtail documentation](https://docs.wagtail.io/en/stable/) is a good place to start.
