# Docker

This directory records best practices for working with [Docker](https://www.docker.com/),
DataMade's preferred container engine.

Looking for templates for your Django/Wagtail application? [Check it out!](https://github.com/datamade/cookiecutter-django-app/)

## Contents

- [Why containers?](#why-containers)
- [Research](research/)
    - [Comparison to existing tools](research/comparisons-to-existing-tools.md)
    - [Recommendation of Adoption](research/recommendation-of-adoption.md)
- [Docker for local development](local-development.md)
- [Useful commands](tips-n-tricks.md)

## Why containers?

Containers are a popular, modern approach to packaging and running software.

They enable developers to ship application code bundled with dependent libraries
and services, ensuring a consistent environment for development and deployment.
This pattern produces applications that are ephemeral – that is, they can be
spun up, run, and removed, irrespective of their environment and other apps
running in it.

Docker is a mature container engine with broad support, including from our
preferred third-party CI services, e.g., Travis-CI and Amazon Web Services,
robust documentation, and an active development community.
