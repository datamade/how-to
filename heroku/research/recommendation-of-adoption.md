# Recommendation of adoption: Heroku

Over the course of the past two months, we've spent time evaluating different possibilities
for containerizing our applications in production. We evaluated:

- ECS (see [Hannah's notes](./hec-log.md))
- Heroku (see [Hannah's notes](./hec-log.md) and [Jean's notes](./jfc-log.md))
- Divio (see [Jean's notes](https://github.com/datamade/how-to/issues/23))

In addition, we considered the possibility of building our own, more incremental
solution, using [Docker Machine and EC2](https://github.com/datamade/how-to/issues/32).

Ultimately, we recommend **moving forward with Heroku as our deployment platform for dynamic client apps**.
According to our research, Heroku does the best job of meeting as many of our
DevOps needs as possible, while being the most easy-to-use and cost-effective
solution that we considered.

Below, we consider these needs in detail, and explain the specifics of why we believe
Heroku to be the right fit for dynamic client apps at DataMade.

## Background: DevOps dreams

During a conversation in May 2019, the DevOps committee discussed and synthesized
our thoughts on [the ways our infrastructure is painful, and how we want to change
it](https://github.com/datamade/devops/issues/90#issuecomment-502196656). We consider
each pain point in detail and explain how Heroku will address it.

### Containerization

**Problem**: Developer environments are containerized, but production environments are not.

Heroku provides first-class support for deploying containers in production with the
[`heroku.yml` config file](https://devcenter.heroku.com/articles/build-docker-images-heroku-yml). With
the proper configuration, Heroku will automatically build and push application
container images to its container registry, and trigger rebuilds of your application
using the latest version of the container image.

Other deployment providers do not offer the same level of container integration that Heroku does.
ECS requires you to maintain your own deployment pipeline for building and pushing
container images, as well as for restarting builds. (It also does not automatically
connect the containers to a load balancer, as Heroku does.) Divio allegedly
supports containerized deployments, but the feature is so new that it is not
documented, and it requires rewriting your Git history to enable.

### Deployment scripts

**Problem**: "Custom deployment scripts are hard to read, write, and maintain."

Heroku deployments are set up entirely through config files. The service abstracts
the process of pushing code to a remote host. Although some amount of infrastructure
setup (such as initializing the Heroku project and connecting it to GitHub) is
still necessary, all of the relevant operations are available in the [Heroku
CLI](https://devcenter.heroku.com/articles/heroku-cli), so while we will no longer
need to maintain deployment scripts for applications, we will likely want to script
the process of setting up a new application.

As mentioned above, ECS still requires custom deployment scripts to build and
push container images. In addition, it requires extra AWS infrastructure, like
load balancers and Route53 hosted zones, in order to work, and this infrastructure
would either have to be set up by hand or (more likely) provisioned with yet
more deployment scripts. Divio purports to offer similar services as Heroku, but
they are undocumented and we were not able to get them to work.

### DNS

**Problem**: DNS is a central point of failure, and is configured separately from
our other infrastructure.

Heroku doesn't really address this problem, unfortunately. While we can use custom
domains with Heroku apps (and Heroku will automatically provision and manage SSL certificates)
we still need to register them with an external registrar.

ECS could mitigate this problem somewhat, since AWS offers [domain registration
services](https://aws.amazon.com/getting-started/tutorials/get-a-domain/) through
its Route53 service. This would at least mean that we could use the same DNS provider
as our infrastructure provider. Divio offers no solutions to this problem.

### SSH

**Problem**: "SSH access is required for provisioning an application", and also for viewing logs.

Heroku exposes SSH access to services through the Heroku CLI. With the Heroku CLI,
developers authenticate through the web app and then shell into running services
with the [`heroku ps:exec` command](https://devcenter.heroku.com/articles/exec).
Since `heroku ps:exec` uses SSH under the hood, the command can be used for tunneling
as well.

### Logging

**Problem**: "Logs are inconsistent, hard to find, and require SSH access to the server."

### Time to first deploy (TTFD)

**Problem**: "Deployment takes too long."

### Permissioning

**Problem**: "User access is granted on a per-application basis, but it's also revoked on a per-application basis."

### Application cleanup

**Problem**: "Applications are hard to clean up."

### Isolation

**Problem**: "Shared services introduce undesirable dependencies between colocated applications."

## Other considerations

There are a few considerations that are important in evaluating any infrastructure
provider. While we didn't bring these up during our DevOps Dreams conversation,
we consider them below out of due diligence.

### Pricing

How affordable is Heroku? How does it compare to AWS?

### Maintenance outlook

There are two pertinent maintenance questions when switching infrastructure providers:

1. How long can we expect the provider to remain stable and cost-effective for us?
2. How hard will it be to maintain existing applications on our old infrastructure provider
   while we switch to a new one?

## Transition plan

How will we transition to Heroku? What are our next steps?
