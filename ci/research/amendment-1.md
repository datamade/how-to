# Recommendation of adoption: CodeDeploy integration for GitHub Actions

In early 2020, [we recommended the adoption of GitHub Actions for contemporary deployments](recommendation-of-adoption.md). Absent a mature integration with CodeDeploy, we recommended apps deployed on legacy infrastructure remain on Travis CI.

As of November, Travis CI throttled compute resources to open source builds, greatly increasing build times from minutes to hours or longer for our public repositories.

As such, we evaluated alternatives based in GitHub Actions and now recommend that apps deployed on legacy AWS EC2 architecture are migrated to GitHub Actions, with deployments via [the `webfactory/create-aws-codedeploy-deployment` action](https://github.com/webfactory/create-aws-codedeploy-deployment).

## Options evaluated

### CodeDeploy actions

In our initial evaluation, the big deal breaker was that we would not be able to integrate with CodeDeploy without writing custom code. As this was a huge pain point for past deployment strategies, I did not want to reintroduce it here, so I did not consider a roll-your-own solution, e.g., [use of the AWS CLI for deployment](https://docs.aws.amazon.com/cli/latest/reference/deploy/create-deployment.html).

Since our initial evaluation, at least two CodeDeploy integrations have emerged:

- [`webfactory/create-aws-codedeploy-deployment`](https://github.com/webfactory/create-aws-codedeploy-deployment)
- [`byu-oit/github-action-codedeploy`](https://github.com/byu-oit/github-action-codedeploy)

Per one of the maintainers, the Webfactory action [was built for internal purposes](https://github.com/datamade/how-to/issues/36#issuecomment-747288650), but it provides useful documentation and is written in clear JavaScript code, making it easy to evaluate and pilot for our own purposes.

The BYU integration may be generalizable, but it appears from the README to be mostly purpose built, with uncertain maintenance futures:

> Hopefully this is useful to others at BYU. Feel free to ask me some questions about it, but I make no promises about being able to commit time to support it.

### Alternative strategies

We also piloted an alternative to direct integration with CodeDeploy: [pushing code bundles to S3 and configuring CodeDeploy to build from the relevant S3 bucket](https://github.com/datamade/how-to/issues/36#issuecomment-736891921).

This is a clever solution involving more configuration than custom code, an advantage. However, it implicates a second AWS service, S3, and the link between S3 and CodeDeploy is invisible, making migration and maintenance somewhat less straightforward than a dropin replacement for deployments via CI.

If we were routinely deploying new apps on AWS infrastructure, this might be acceptable. The reality is that this change mostly implicates legacy apps with limited maintenance budgets, so ease of use is a top priority.

With all of that said, if for any reason we decide to abandon direct integration with CodeDeploy, the S3 -> CodeDeploy pattern could be a reasonable fallback.

## Proof of concept

I piloted `webfactory/create-aws-codedeploy-deployment` in the Metro project suite:

- [`la-metro-councilmatic`](https://github.com/datamade/la-metro-councilmatic)
    - https://github.com/datamade/la-metro-councilmatic/pull/678
    - https://github.com/datamade/la-metro-councilmatic/pull/682
    - https://github.com/datamade/la-metro-councilmatic/pull/684
- [`la-metro-dashboard`](https://github.com/datamade/la-metro-dashboard)
    - https://github.com/datamade/la-metro-dashboard/pull/67

## Tradeoffs

Advantages of GitHub Actions for legacy apps:

- Overall build time reduced from hours to minutes versus Travis CI
- Consistent deployment practices for apps, regardless of the infrastructure they're deployed on
- The Webfactory integration can create deployment groups on the fly, enabling a behavior similar to Heroku review apps (if we wanted it)

Disadvantages of GitHub Actions for legacy apps:

- The Webfactory integration does not support deployments from tags, so we have to switch to deployments from a branch

## Maintenance outlook

Webfactory [is a software development company in Germany](https://www.webfactory.de/en/). As with any free and open-source software, there is always the risk that the maintainers could choose to shelve or even sunset the code. Some positive signs on this front:

- The current iteration of the integration works for our purposes. This will only ever not be the case if AWS makes material changes to its API.
- When we did encounter a problem, [the maintainer was responsive and friendly](https://github.com/webfactory/create-aws-codedeploy-deployment/issues/5), offered a stopgap solution, and ultimately cut a new release with a fix.
- Per the maintainer, the integration [was developed for internal use](https://github.com/datamade/how-to/issues/36#issuecomment-747288650). While it's still young and relatively untested, they have plans to adopt it more broadly, a good thing for mid- to long-term maintenance.

If there is ever a need to switch away from this pattern, removing it is as simple as deleting a few lines in a GitHub workflow.
