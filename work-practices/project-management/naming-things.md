# The subtle art of naming things

> There are only two hard things in Computer Science: cache invalidation and
> naming things.
> - [As quoted by Martin Fowler](https://martinfowler.com/bliki/TwoHardThings.html)

We here at DataMade have worked laboriously over the past couple years to get
our deployment practices setup in such a way that things are generally
automated. One of the hard lessons was finding all the ways in which naming
some component in the deployment pipeline could come back to bite us when we
tried to automate it. This is an attempt at compiling a handy little guide to
the practices that we've come up with for naming things so that when you're
getting ready to start deploying the project you're working on, things should
"just work".

### Github repository

Repositories should typically follow directory naming standards, which is to say
they should be lowercase and have words delimited with hyphens (`-`).

Beyond the syntax of the name, take time to choose a name here that
will make sense to you in 6 months and will make sense to other people
(especially if the project is open source). Since the Github repository is
often the first artifact that is created for a project, this is what we use as
the name for all of the other services and integrations that we'll configure,
such as Sentry, CodeDeploy, Travis, and Semaphor. Put another way: When you set
up integrations with your project, you must use the name of the Github
repository. Choose wisely...

A good repository name might look like:

- `my-excellent-project`

Bad repository names might include:

- `MyExcellentProject`
- `my_excellent_project`
- `mepv2.0`

### CodeDeploy application and deployment groups

As mentioned above, when you are configuring CodeDeploy, make sure you use the
name of the Github repository as the name of the application. For the
deployment groups, we use `staging` and `production`.

### Configuration files

Within your project, you'll have configuration files for services like Nginx
and Supervisor. Those follow a naming convention as well:

`<github repository name>-<deployment group>.conf.<service name>`

So, if you're making a Supervisor configuration file for `example-project` for the
`staging` deployment group, the name will look like:

`example-project-staging.conf.supervisor`

### Staging hostname

For the staging environment, we usually use a `datamade.us` subdomain. This
should also match the name of the Github repository. So:

`example-project.datamade.us`

### Sentry project

This one is easy: Just use the Github repository name.
