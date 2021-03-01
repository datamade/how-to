# Literate Analysis and RMarkdown

This directory records best practices for writing literate analysis reports and using
[RMarkdown](https://rmarkdown.rstudio.com/authoring_quick_tour.html) to do it.

Literate analysis is a style of writing documents that includes the text and the code for analysis in one document. It is a major benefit in keeping your numbers and figures
aligned with your text; consolidating your work sanely; and self-documenting the code
your analysis code. See [Hannah write up for some more depth](https://source.opennews.org/articles/black-box-be-gone-tools-human-optimized-data-analy/).

## Contents

- README
- [Research](./research/)
    - [Comparisons with existing tools](./research/comparisons-with-existing-tools.md)
    - [Recommendation of adoption](./research/recommendation-of-adoption.md)

## When to Literate Analysis

When you have to write code to generate figure, charts, or graphics to include in 
a research report, you should write a literate analysis document. 

## How to use RMarkdown for Literate Analysis

Look to the [Courts Transparency cookiecutter](https://github.com/datamade/cookiecutter-court-transparency) for inspiration in getting started.

If this is your first project, we strongly recommend using [RStudio](https://rstudio.com/), which has fabulous support for RMarkdown.

## Resources for learning

* https://rmarkdown.rstudio.com/lesson-1.html