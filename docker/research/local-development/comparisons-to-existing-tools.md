## Comparison to existing tools

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
