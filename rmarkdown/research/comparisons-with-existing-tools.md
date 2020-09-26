# Comparing rMarkdown with existing tools

How does rMarkdown compare with existing tools in DataMade's stack or possible alternatives.

## Pweave

Like rMarkdown, [Pweave](http://mpastell.com/pweave/) is an implementation of [noweb](https://en.wikipedia.org/wiki/Noweb), but one that primarily targets Python instead of R.

The main advantage of Pweave is that it is Python. 

While rMarkdown does allow for Python code chunks, there is typically some setup code and that does need to in R. With Pweave, it's all Python.

That is really the only advantage.

Like rMarkdown requires an additional runtime beyond standard Python. rMarkdown requires R and Pweave requires
[IPython](https://ipython.org/).

Pweave is not actively maintained, and has not been updated
in three years.

rMarkdown has better editor support than Pweave. For the following editors, rMarkdown is as good and usually better
than support for Pweave, if there any Pweave support exists.

* [sublime](https://packagecontrol.io/packages/knitr)
* [emacs](https://ess.r-project.org/)
* [atom](http://www.goring.org/resources/atom_and_r.html)
* [vscode](https://marketplace.visualstudio.com/items?itemName=Ikuyadeu.r)

rMarkdown also has its own IDE, [RStudio](https://rstudio.com/)

Beyond active devlopment and editor support, Pweave is missing many features compared to rMarkdown. Of greatest consequence are 1. chunk specific caching and support for 2. multiple languages, particularly SQL.

Chunk specific caching can dramatically reduce build times which is critical in speed of development.

Our past experience suggests that SQL will be a common language we will use in literate reports, and first class
support is very nice.

## Jupyter Notebook

Jupyter Notebooks overlap in functionality with rMarkdown. The main differences is that Notebooks are intended to be
an interactive exploration tools and rMarkdown is intended to be a documentation and document creation tool. 

I have not used Notebooks extensively, but three attributes
make it less attractive.

1. While possible, it is more difficult to generate attractive documents from Notebooks.
2. The file format of Notebooks is not plain text and not natively diffable by github or gitlab, thus making PRs difficult
3. While possible, Notebooks are not primarily intended to
be scripted instead of interactive, thus making bit of mismatch with our ETL philosophy

## Manual integration

We can do and do generate statistics and graphs in one tool and then copy the data or graphics into Google Docs or a markdown file. Sometimes this is the appropriate approach, in
the recommendation document.