# GatsbyJS

This directory records best practices for working with [GatsbyJS](https://github.com/datamade/tutorials/projects/1), a static site generator built on top of React and GraphQL.

**Our cookiecutter for creating a new Gatsby app lives in the [containerization templates](https://github.com/datamade/how-to/tree/master/docker/templates) directory.**

## Contents

- README
    - [When to use Gatsby](#when-to-use-gatsby)
    - [How to use Gatsby](#how-to-use-gatsby)
    - [Resources for learning](#resources-for-learning)
- [Research](./research/)
    - [Comparisons with existing tools](./research/comparisons-with-existing-tools.md)
        - [Gatsby vs. Jekyll](./research/comparisons-with-existing-tools.md#gatsby-vs-jekyll)
        - [Gatsby vs. Django](./research/comparisons-with-existing-tools.md#gatsby-vs-django)
    - [Recommendation of adoption](./research/recommendation-of-adoption.md)
- [Stack](stack.md)
    - [Tools in our Gatsby development stack](stack.md)
    - [Some example setups](stack.md#some-example-setups)
    - [Managing packages and plugins](stack.md#managing-packages-and-plugins)

## Standard toolkit

| Objective | Library | Internal documentation |
| :- | :- | :- |
| Data Visualization | [`recharts`](http://recharts.org/) | |
| Error Logging | [`@sentry/gatsby`](https://www.gatsbyjs.com/plugins/@sentry/gatsby/) | [Link](./../logging/sentry.md#logging-errors-in-gatsby-applications) |

## When to use Gatsby

Gatsby is an excellent choice for two types of projects:

1. Static sites (that is, sites that can be deployed with pure HTML/CSS/JavaScript)
2. Small dynamic sites with a limited range of simple server-side functions **not** including faceted search, user administration, or admin interfaces

For more details on the specific pros and cons of Gatsby, see the [comparisons with existing tools](./research/comparisons-with-existing-tools.md) produced during R&D.

## How to use Gatsby

To start a Gatsby project, [create a new repository from our Static App Template](https://github.com/datamade/static-app-template/generate). Once you're ready to publish the site, follow our guide to [deploy a static site](https://github.com/datamade/deploy-a-site/blob/master/Deploy-a-static-site.md).

For an example of a DataMade app deployed with Gatsby, see [LISC CNDA](https://github.com/datamade/lisc-cnda).

## Resources for learning

The following is a list of good resources for learning how to use Gatsby.

- [The Gatsby.js tutorial](https://www.gatsbyjs.org/tutorial/) - Gatsby's official tutorial. A full walkthrough of building a simple blog from scratch in Gatsby, including quick sidebars on the basics of React, JSX, and GraphQL.
- [The React docs](https://reactjs.org/docs/hello-world.html) - A step-by-step guide through the basics of React. Useful for getting your bearings in JSX, components, and React state management, which are important prerequisites for Gatsby.
- [The Fullstack Tutorial for GraphQL](https://www.howtographql.com/) - Gatsby's recommended tutorial for learning GraphQL. We recommend reading the "GraphQL fundamentals" section.
- [@jeancochrane's lunch&learn on Gatsby](https://gist.github.com/jeancochrane/705dda18da74fafe4b8182d15284114d) - A set of brief notes giving a quick overview of Gatsby's features.

See our documentation on [the Gatsby development stack](stack.md) for more on how we organize Gatsby applications and manage JavaScript dependencies at DataMade.
