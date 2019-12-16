## Setting up your environment

This is a list of common tools that DataMade uses. You should install these on your machine and keep them up to date.

**Linux users**: Most of these tools are available as aptitude packages. When possible, prefer binary packages to building from source.

**Mac users**: Most of these tools are available as [Homebrew](http://brew.sh/) packages. Homebrew is by far the easiest way to manage packages on OS X.

### Version control

We use GitHub and Git to keep our work under version control. Note that we prefer the `git` CLI to the GitHub desktop GUI.

### Packages

* [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

### Python

DataMade recommends you do all of your Python work in virtual environments (virtualenvs). Virtualenvs help enforce dependency separation between your projects, making it a lot easier for other users to replicate your work.

The simplest way to manage Python with minimal headaches is to do a clean install of Python via homebrew or apt. Get pip and virtualenvwrapper running on your fresh version of Python. Then, `mkvirtualenv gus` (**G**enerally **U**seful **S**tuff). `workon gus` whenever you want to use "global" packages, and `workon <project>` when developing a specific project.

#### Packages

* Python 3
* [pip](https://pip.pypa.io/en/stable/installing/)
    * Make sure you're using [the latest version of pip](https://pip.pypa.io/en/stable/installing/#upgrading-pip). (If you used homebrew to install Python, you got pip for free.)
* [virtualenv](https://virtualenv.pypa.io/en/stable/)
* [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html#basic-installation)
    * virtualenvwrapper contains useful shortcut commands for all stages of virtualenv use. [Install it](https://virtualenvwrapper.readthedocs.io/en/latest/install.html#basic-installation), making sure to follow the instructions for editing your shell startup file.
    * If you run into ownership errors and you installed Python via Homebrew, add `VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python3` to your shell startup file prior to the lines you added for virtualenvwrapper, and try again.

### Text Editor

Most of us use Sublime as our text editor of choice. If you do, too, then you will need to make some modifications to your settings.

In the nav, under "Sublime Text," you will find a "Preferences" fly open, where you will see "Settings - User." Here, you can override the default settings (i.e., do not make changes to the "Settings - Default" file). In the User file, add two things:

* "trim_trailing_white_space_on_save": false,
* "tab_size": 4,

Note: You are welcome to explore other text editor options, e.g., Atom, Vim, etc.

### Data

We try to maintain a consistent and standardized toolkit for all of our data work. We know that there are many good options for working with data, and we are always open to hearing arguments for new additions to this toolkit. But these tools have stood the test of time, and you'll see them crop up over and over in DataMade's work.

#### Packages

* Bash/Unix
     * Comes installed with OS X, macOS, Windows 10, and all Linux distributions.
* [PostgreSQL](https://www.postgresql.org/)
     * A powerful open-source database engine (also known as Postgres). There are a million ways to download and manage Postgres, but you'll be best off installing it with your package manager and following the [getting started guide](https://www.postgresql.org/docs/9.6/static/tutorial-arch.html) to configure it.
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
* [PostGIS](http://www.postgis.net/)
     * A geospatial plugin for Postgres. We do lots of geographic work, so it's worth installing this as soon as you have Postgres up and running. Ignore the installers and install with your [favorite package manager](http://postgis.net/install/); make sure to install the version that corresponds to your version of Postgres, and remember that PostGIS must be activated in any database that needs to use it by running the SQL command `CREATE EXTENSION postgis`.
* [GDAL](http://www.gdal.org/)
     * A set of command line tools for modifying and converting geospatial data. If you're on a Mac, make your life easier and [install it with homebrew](https://trac.osgeo.org/gdal/wiki/BuildingOnMac). (If you installed PostGIS via homebrew, you got GDAL, too.)
* [QGIS](http://www.qgis.org/en/site/)
     * The best open-source GUI app for playing with geospatial data. (Eat your heart out, ESRI.) Currently there are no perfect ways of installing QGIS. We've had some success with the [homebrew package on macOS](http://usabilityetc.com/2016/06/how-to-install-qgis-with-homebrew/) and [William Kyngsburye's installers](http://www.kyngchaos.com/software/qgis).
* [csvkit](https://csvkit.readthedocs.io/en/1.0.1/)
     * Command line tools for working with CSVs, the most common (and arguably the best) file format for spreadsheets. It's built on Python, so you can install it by running `pip install csvkit` in your `gus` virutalenv.

### Security

Cryptographic security is essential for developers. You don't have to know the guts of how these tools work, but you should have them installed and you should be comfortable using them whenever possible.

To enable hard drive encryption on a Macbook, go to System Preferences > Security & Privacy > FileVault. Turn on FileVault and save a recovery key, as opposed to backing up in your iCloud account, in a safe place (such as LastPass). The process will take some time, probably about a day depending on what you're doing and what model computer you have. It can run in the background as long as your computer is awake and connected to power.

#### Packages

* [SSH](http://linuxcommand.org/man_pages/ssh1.html)
     * Secure Shell, a protocol for communicating securely over unsecured networks. We use it to push and pull from Git remotes and to access our servers. It comes pre-installed as a command line tool on all Mac and Linux distributions; [generate an SSH key](https://help.github.com/articles/generating-an-ssh-key/) if you haven't already and follow the instructions for adding it to your GitHub account.
* [GPG](https://www.gnupg.org/)
     * GNU Privacy Guard, a command line tool for encrypting and decrypting files. If you prefer GUIs, install it and generate a new key via [GPG Suite](http://notes.jerzygangi.com/the-best-pgp-tutorial-for-mac-os-x-ever/). Otherwise, Mac users can `brew install gnupg2`, while enthusiasts of the "subtler arts of computing" can [compile it](https://www.gnupg.org/download/index.en.html), then [configure your key](https://keyring.debian.org/creating-key.html) by hand.
* [Blackbox](https://github.com/StackExchange/blackbox)
     * StackExchange's open-source CLI for keeping secrets secure under public version control. Follow [our excellent guide](https://github.com/datamade/deploy-a-site/blob/master/Setup-blackbox.md) (internal link) to use it.

### Static sites

Most of our sites are dynamic and built on Django, but sometimes we deploy small static sites (like [datamade.us](https://datamade.us)) using Jekyll, a site generator built on Ruby. To run these sites locally, you'll need to install some OS-level Ruby dependencies.

* [Ruby](https://www.ruby-lang.org/en/downloads/)
     * We recommend using a third-party Ruby package manager like [RVM](https://rvm.io/) (follow the unofficial cheat sheet [linked from their website](http://cheat.errtheblog.com/s/rvm), being sure to run `rvm install x.x.x` when you come to it with [the latest version of Ruby](https://www.google.com/search?q=latest+version+of+ruby)) or [rbenv](http://octopress.org/docs/setup/rbenv/) to manage different versions of Ruby.(http://octopress.org/docs/setup/rbenv/) to manage different versions of Ruby.
* Bundler (`gem install bundler`)
     * Bundler is Ruby's package manager, and it works a lot like pip.
* [Jekyll](https://jekyllrb.com/)
     * A static site generator built on Ruby. Always check the Gemfile of the project you're working on to see which version of Jekyll you need to run. If you have multiple versions of Jekyll installed, you may have to prepend Jekyll commands with `bundle exec` (e.g. `jekyll serve` becomes `bundle exec jekyll serve`).
