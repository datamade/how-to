# Docker

This directory records best practices for working with [Docker](https://www.docker.com/),
DataMade's preferred container engine.

## Contents

- [Why containers?](#why-containers)
- [Comparison to existing tooling](#comparison-to-existing-tooling)
- [Docker for local development](local-development.md)

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

## Comparison to existing tooling

DataMade does not employ a single tool analogous to containers, however some of
our current practices intend to solve similar problems.

### Consistent development environments

It is DataMade's current practice to achieve consistent Python environments
across machines by declaring application dependencies in `requirements.txt`
files and installing those dependencies in application-specific virtual
environments.

#### Pros

- `requirements.txt` files cannot declare non-Python dependencies. By contrast,
Docker allows developers to declare as a dependency virtually any software
available for download on the Internet.
- In addition to dependencies, Docker containers can include application
configurations and run setup scripts, such as database migrations. This
drastically decreases the time it takes to get an app up and running for
local testing and development.
- Docker makes it easy to manage multiple installations of Python and external
services, like Solr and Postgres. This is especially useful for local
development of applications that depend on older versions, and for the
installation of Python libraries that are picky about the environment of the
host machine, e.g., `psycopg<2.7` will fail to build if Postgres > 9 is
installed.
- `docker-compose.yml` files are conceptually similar to Makefiles in that
you declare "recipes" for your application processes and services, then specify
how they depend on each other, such that the application can be run with a
single command. This is both more convenient and more explicit than manually
running a series of commands within a virtual environment.

#### Cons

- Dockerfiles and `docker-compose.yml` files are necessarily more complex than
listing Python depedencies in a text file. There is a learning curve to
overcome when reading and writing Docker configurations, in particular for
developers unfamiliar basic Unix networking and/or system administration tasks.

## Proposed pilot

We have containerized a local version of Dedupe.io, as well as its test suite,
using the `docker-compose.yml` files. This pattern has enabled both of us to
get Dedupe.io up and running on new computers in minutes, a vast improvement
over virtual environments and manual installation of external services.

We recommend using a containerized development environment for the next new
website we build, while continuing to use the containerized environment for
Dedupe.io development.
