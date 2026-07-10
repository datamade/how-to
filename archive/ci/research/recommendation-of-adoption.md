# Recommendation of adoption: GitHub Actions

Based on our research, we recommend adopting GitHub Actions as our CI service of choice for **apps deployed on Heroku and Netlify**.

~For apps deployed on our legacy AWS EC2 infrastructure, we recommend sticking with Travis CI until a well-supported Action for working with CodeDeploy becomes available.~

**Note:** We originally recommended continued use of Travis CI for apps deployed on legacy AWS EC2 infrastructure, however Travis CI [recently deprioritized open source builds](https://blog.travis-ci.com/2020-11-02-travis-ci-new-billing), leading to build times on the order of hours or days. We now recommend migrating legacy applications under continued development from Travis CI to GitHub Actions. See [Amendment 1](amendment-1.md) for further research, and [our documentation on GitHub Actions](../github-actions.md) for examples and starter code.

The following document records our recommended path forward for adopting GitHub Actions.

## Proof of concept

As proof of concept, we tested GitHub Actions on a few different projects:

- [`pytest-flask-sqlalchemy`](https://github.com/jeancochrane/pytest-flask-sqlalchemy/commit/b6b9f846977e7981a0ec69d969eceb99ddee58f7), a Python library deployed to PyPi
- [`mn-election-archive`](https://github.com/datamade/mn-election-archive/pull/58), a Django app deployed on Heroku
- [`document-search`](https://github.com/datamade/document-search/pull/28), a Django app deployed on AWS EC2 with CodeDeploy

## Prerequisite skills

GitHub Actions requires fluency in YAML, which is also required for Travis CI. It also requires that developers be familiar with the [workflow syntax for GitHub Actions](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/workflow-syntax-for-github-actions), which is more flexible than Travis' language but has a steeper learning curve as a result.

To deal with this learning curve, we aim to produce clear documentation and templates that developers can use to quickly bootstrap a GitHub Actions configuration.

## Tradeoffs

Advantages of GitHub Actions:

- Native support for containerized deployments
- Built in to our source control provider
- Cheaper than Travis CI

There are a few downsides to GitHub Actions:

- ~No CodeDeploy integration~
- Workflow syntax is more complicated
- No container layer caching

Due to these tradeoffs, we think that GitHub Actions is an appropriate choice ~for apps that are not deployed with CodeDeploy. We will keep an eye out for CodeDeploy integrations, but until those arrive, we plan to continue supporting Travis CI for our legacy AWS EC2 infrastructure~.

## Maintenance outlook

GitHub Actions is a low-risk choice of service because it is integrated with GitHub, the third-party service that we depend on the most. However, this adoption will create a situation for at least some amount of time where we have to maintain projects on two CI services, GitHub Actions and Travis, which could potentially make long-term maintenance tricky.

This situation feels tenable because we have a substantial amount of written documentation for Travis CI along with a lot of developer expertise. ~We don't expect that existing Travis projects will be hard to maintain, even in a future where we're almost exclusively using GitHub Actions for new apps.~
