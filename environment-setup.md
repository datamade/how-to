# 💻 Setting up your development environment

There are many guides to setting up your computer for development. Each has its own merits. At DataMade, we perform a mix of maintaining legacy projects and developing new projects, often in parallel. Our toolkit is therefore optimized for managing many, isolated versions of packages and getting up and running on new projects quickly.

#### Contents

- [Version control](#version-control)
- [Text editor](#text-editor)
- [Python](#python)
- [Docker](#docker)
- [Security](#security)
- [Data](#data)
- [Geospatial data](#geospatial-data)
- [Static sites](#static-sites)

For Linux users, most of these tools are available as aptitude packages. When possible, prefer binary packages to building from source. For Mac users, most of these tools are available as [Homebrew](http://brew.sh/) packages. Homebrew is by far the easiest way to manage packages on OS X.

## Version control

We use GitHub and Git to keep our work under version control. Note that we prefer the `git` CLI to the GitHub desktop GUI.

#### Packages

* [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

## Text editor

Most of us use Sublime as our text editor of choice. If you do, too, then you will need to make some modifications to your settings.

In the nav, under "Sublime Text," you will find a "Preferences" fly open, where you will see "Settings - User." Here, you can override the default settings (i.e., do not make changes to the "Settings - Default" file). In the User file, add two things:

```json
    "trim_trailing_white_space_on_save": false,
    "tab_size": 4,
```

‼ **Note:** You are welcome to explore other text editor options, e.g., Atom, Vim, etc.

#### Packages

* [Sublime Text 3](https://www.sublimetext.com/3)

## Python

At DataMade, you'll run most Python processes in containers. However, it's still useful to have a fresh install of Python on your machine to keep your system Python isolated (it's important!) and to use a later version of Python (if you're on a Mac, your system Python is probably version 2.7).

When you aren't using containers, DataMade recommends you conduct Python work in virtual environments (virtualenvs). Virtualenvs help enforce dependency separation between your projects and make it a lot easier for other users to replicate your work on their computers. The Python ecosystem contains a lot of options for managing your environments, from the built-in `virtualenv` package to bundled package and environment management with `conda`. As traditionalists, we like `virtualenvwrapper`, which provides a few convenience functions you can use from your terminal to create, activate, deactivate, and remove virtual environments.

Finally, to install packages in your environment, you'll need `pip`, _the_ Python package installer.

The simplest way to manage Python with minimal headaches is to do a clean install of Python via homebrew or apt, then get `pip` and `virtualenvwrapper` running on your fresh version of Python.

Optionally, create a global virtual environment for general utility packages:

```bash
mkvirtualenv gus  # that is, generally useful stuff
```

`workon gus` whenever you want to use these "global" packages. More often, you'll want to create project-specific virtual environments, and `workon` those environments during development.

#### Packages

* Python 3
* [pip](https://pip.pypa.io/en/stable/installing/)
    * Make sure you're using [the latest version of pip](https://pip.pypa.io/en/stable/installing/#upgrading-pip). (If you used homebrew to install Python, you got pip for free!)
* [virtualenv](https://virtualenv.pypa.io/en/stable/)
* [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html#basic-installation)
    * virtualenvwrapper contains useful shortcut commands for all stages of virtualenv use. [Install it](https://virtualenvwrapper.readthedocs.io/en/latest/install.html#basic-installation), making sure to follow the instructions for editing your shell startup file.
    * If you run into ownership errors and you installed Python via Homebrew, add `VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python3` to your shell startup file prior to the lines you added for virtualenvwrapper, and try again.

## Docker

Containers are a popular, modern approach to packaging and running software. We use the Docker engine to create, run, and destroy containers for our applications during local development. This makes it infinitely easier to manage dependencies across 5+ years of web applications.

#### Packages

* [Docker Community Edition](https://www.docker.com/products/container-runtime)
     * A popular and feature-rich container engine. [Mac users, look no further for installation instructions](https://docs.docker.com/v17.09/docker-for-mac/install/). Unix users, open the Mac instructions and find your distribution in the sidebar.

## Security

Cryptographic security is essential for developers. You don't have to know the guts of how these tools work, but you should have them installed and get comfortable using them.

To enable hard drive encryption on a Macbook, go to System Preferences > Security & Privacy > FileVault. Turn on FileVault and save a recovery key in a safe place, such as LastPass. The process will take some time, probably about a day depending on what you're doing and what model computer you have. It can run in the background as long as your computer is awake and connected to power.

#### Packages

* [SSH](http://linuxcommand.org/man_pages/ssh1.html)
     * Secure Shell, a protocol for communicating securely over unsecured networks. We use it to push and pull from Git remotes and to access our servers. It comes pre-installed as a command line tool on all Mac and Linux distributions; [generate an SSH key](https://help.github.com/articles/generating-an-ssh-key/) if you haven't already and follow the instructions for adding it to your GitHub account.
* [GPG](https://www.gnupg.org/)
     * GNU Privacy Guard, a command line tool for encrypting and decrypting files. Mac users can `brew install gnupg2`, while enthusiasts of the "subtler arts of computing" can [compile it](https://www.gnupg.org/download/index.en.html). Then, [configure your key](https://keyring.debian.org/creating-key.html) by hand.
* [Blackbox](https://github.com/StackExchange/blackbox)
     * StackExchange's open-source CLI for keeping secrets secure under public version control. Follow [our excellent guide](https://github.com/datamade/deploy-a-site/blob/master/Setup-blackbox.md) (internal link) to use it.

## Data

We try to maintain a consistent and standardized toolkit for all of our data work. We know that there are many good options for working with data, and we are always open to hearing arguments for new additions to this toolkit. But these tools have stood the test of time, and you'll see them crop up over and over in DataMade's work.

🚨  **Note:** If you're working on a new DataMade application, most of these dependencies (e.g., Postgres) should be containerized, i.e., you don't need to install them directly on your computer, and you can skip this section. If you're working on a legacy application that does not include containerization artifacts, read on for our installation tips.

#### Packages

* Bash/Unix
     * Comes installed with OS X, macOS, Windows 10, and all Linux distributions.
* [PostgreSQL](https://www.postgresql.org/)
     * A powerful open-source database engine (also known as Postgres). There are a million ways to download and manage Postgres. If you're writing a new application, this dependency should be containerized, i.e., you don't need to install it directly on your machine. but you'll be best off installing it with your package manager and following their [Getting Started guide](https://www.postgresql.org/docs/9.6/static/tutorial-arch.html) to configure it.
         * Many of our database configurations assume your installation of Postgres has a `postgres` database owned by a `postgres` user. After you've installed Postgres via your favorite package manager (probably `brew install postgresql`), run the following commands from your terminal:

             ``` bash
             createuser -s postgres # create postgres superuser
             createdb -O postgres postgres # create postgres database owned by postgres user
             ```
           If you get a "database already exists" error:

             ```bash
             psql # log in to postgres
             alter database postgres owner to postgres; # make postgres the owner of the postgres database
             ```
* [csvkit](https://csvkit.readthedocs.io/en/1.0.1/)
     * Command line tools for working with CSVs, the most common (and arguably the best) file format for spreadsheets. It's built on Python, so you can install it by running `pip install csvkit` in your `gus` virutalenv.

## Geospatial data

🚨  **Note:** If you're working on a new DataMade application, most of these dependencies (e.g., PostGIS) should be containerized, i.e., you don't need to install them directly on your computer, and you can skip this section. If you're working on a legacy application that does not include containerization artifacts, read on for our installation tips.

#### Packages

* [PostGIS](http://www.postgis.net/)
     * A geospatial plugin for Postgres. We do lots of geographic work, so it's worth installing this as soon as you have Postgres up and running. Ignore the installers and install with your [favorite package manager](http://postgis.net/install/); make sure to install the version that corresponds to your version of Postgres, and remember that PostGIS must be activated in any database that needs to use it by running the SQL command `CREATE EXTENSION postgis`.
* [GDAL](http://www.gdal.org/)
     * A set of command line tools for modifying and converting geospatial data. If you're on a Mac, make your life easier and [install it with homebrew](https://trac.osgeo.org/gdal/wiki/BuildingOnMac). (If you installed PostGIS via homebrew, you got GDAL, too.)
* Optional: [QGIS](http://www.qgis.org/en/site/)
     * The best open-source GUI app for playing with geospatial data. Currently there are no perfect ways of installing QGIS. We've had some success with the [homebrew package on macOS](http://usabilityetc.com/2016/06/how-to-install-qgis-with-homebrew/) and [William Kyngsburye's installers](http://www.kyngchaos.com/software/qgis).

## Static sites

Most of our sites are dynamic and built on Django, but sometimes we deploy small static sites (like [datamade.us](https://datamade.us)) using Jekyll, a site generator built on Ruby, or more recently, [GatsbyJS](https://www.gatsbyjs.org/tutorial/).

🚨 **Note:** If you're working on a new DataMade application, all of these dependencies should be containerized, i.e., you don't need to install them directly on your computer, and you can skip this section. If you're working on a legacy application that does not include containerization artifacts, read on for our installation tips.

#### Packages

* [Node.js](https://nodejs.org/en/)
     * An environment to run JavaScript outside the browser, bundled with its very own package manager, [`npm`](https://www.npmjs.com/). For Mac users, installation is as simple as `brew install node`.
* [GatsbyJS](https://www.gatsbyjs.org/)
     * A React-powered static site generator that works with a variety of data sources. The GatsbyJS team provides [excellent documentation for installation](https://www.gatsbyjs.org/tutorial/part-zero/) and getting your feet wet.
* [Ruby](https://www.ruby-lang.org/en/downloads/)
     * We recommend using a third-party Ruby package manager like [RVM](https://rvm.io/) (follow the unofficial cheat sheet [linked from their website](http://cheat.errtheblog.com/s/rvm), being sure to run `rvm install x.x.x` when you come to it with [the latest version of Ruby](https://www.google.com/search?q=latest+version+of+ruby)) or [rbenv](http://octopress.org/docs/setup/rbenv/) to manage different versions of Ruby.(http://octopress.org/docs/setup/rbenv/) to manage different versions of Ruby.
* Bundler (`gem install bundler`)
     * Bundler is Ruby's package manager, and it works a lot like pip.
* [Jekyll](https://jekyllrb.com/)
     * A static site generator built on Ruby. Always check the Gemfile of the project you're working on to see which version of Jekyll you need to run. If you have multiple versions of Jekyll installed, you may have to prepend Jekyll commands with `bundle exec` (e.g. `jekyll serve` becomes `bundle exec jekyll serve`).
