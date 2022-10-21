# 🐍 Python

This directory contains research and best practices related to our favorite programming language, Python.

### Contents

- [Python project documentation](#python-project-documentation)

## Python project documentation

At DataMade, we believe in [better living through documentation](https://datamade.us/blog/better-living-through-documentation/). For Python projects (libraries and Django projects alike), we recommend writing documentation using [Sphinx](https://www.sphinx-doc.org/en/master/index.html) and [`autodoc`](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html), and hosting that documentation on [Read the Docs](https://readthedocs.org/).

### When to write docs

Documentation is crucial for software intended to be used by others. That means open-source libraries and projects we plan to hand off to other developers should be documented.

While docs are discretionary for internal projects, we highly recommend documenting a minimum of system and application dependencies and local development instructions. These are included in [the DataMade README template](https://github.com/datamade/readme-template). 

**If your project calls for docs, don't wait to start writing!** It's much easier to write docs as you implement new features than it is to retroactively document an entire codebase.

### Sphinx and autodoc

[Sphinx](https://www.sphinx-doc.org/en/master/index.html) is a Python documentation generator. [Its autodoc extension](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html) allows you to interweave prose with docstrings from your code in your final documentation.

Use [the Sphinx quickstart documentation from ReadTheDocs](https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html) generate the files you'll need to compose your documentation, then add your first draft to `docs/index.rst`. See [the reStructuredText spec](https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html) and [autodoc documentation](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html), respectively, for more on correctly formatting your documentation file/s and how to leverage autodoc to include content from your docstrings.

See the [`census_area.core` module](https://github.com/datamade/census_area/blob/master/census_area/core.py) and [`docs/index.rst`](https://raw.githubusercontent.com/datamade/census_area/master/docs/index.rst) for an example of combined documentation, powered by this stack.

### Deploying your docs

To deploy your documentation, you will need to [sign up for Read the Docs using your GitHub account](https://readthedocs.org/accounts/signup/). Then, follow [the instructions for importing documentation to Read the Docs](https://docs.readthedocs.io/en/stable/tutorial/index.html#first-steps) to deploy your docs.

By default, your docs will be rebuilt on each commit to your default branch (e.g., `master` or `main`). You can customize the default branch on the Read the Docs site by going to `${YOUR_PROJECT}` > Admin > Advanced settings, and selecting the branch you want to autobuild from.

You can also [configure Read the Docs to build your docs on pull requests](https://docs.readthedocs.io/en/stable/pull-requests.html) so you can preview changes before you deploy them.

See the [`census_area`](https://github.com/datamade/census_area) and [`dedupe`](https://github.com/dedupeio/dedupe) packages for examples of projects configured to be deployed to Read the Docs. 
