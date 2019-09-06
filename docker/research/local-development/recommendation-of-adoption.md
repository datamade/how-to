# Recommendation of adoption: Docker

We recommend use of Docker and `docker-compose` for local development of both
static and dynamic sites.

## Proof of concept and pilot

We containerized a local version of Dedupe.io, as well as its test suite,
as a proof of concept. This pattern enabled us to get Dedupe.io up and running
on new computers in minutes, a vast improvement over virtual environments and
manual installation of external services.

We recommended piloting containerized development environments on new projects,
while continuing to use the containerized environment for Dedupe.io development.
During this period, we containerized:

- [🏡 `ihs-website-v2`](https://github.com/datamade/ihs-website-v2)
- [🏆 `lisc-cdna`](https://github.com/datamade/lisc-cnda)
- [🎁 `dedupe.io`](https://github.com/dedupeio/dedupe.io)

## Prerequisite skills

Containerization requires some knowledge of a few working areas. Chief among
them are Docker and `docker-compose`, as well as some networking basics.

### Docker and `docker-compose`

Docker is a well-documented tool. We recommend that new developers spend half an
hour with Parts 1-3 of Docker's [Getting Started documentation](https://docs.docker.com/get-started/)
to acquaint themselves with core concepts. We will also lead a learning lunch
on the patterns set out in this documentation.

### Networking

`docker-compose` implies several services that work together to run an app.
They communicate [through networking](https://docs.docker.com/config/containers/container-networking/).
To understand the defaults, as well as what they mean for app configuration and
when you need to customize them, it helps to have a working knowledge of
host names and ports. Definitions for these networking terms are myriad. I like
the ones from whatismyipaddress.com:

- [hostname](https://whatismyipaddress.com/hostname)
- [port](https://whatismyipaddress.com/port)
