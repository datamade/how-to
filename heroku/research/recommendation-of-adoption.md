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

### Deployment scripts
Problem: "Custom deployment scripts are hard to read, write, and maintain."

### DNS
Problem: Central source of failure.

### SSH
Problem: "SSH access is required for provisioning an application", and also viewing logs.

### Logging
Problem: "Logs are inconsistent, hard to find, and require SSH access to the server."

### Time to first deploy (TTFD)
Problem: "Deployment takes too long."

### Permissioning
Problem: "User access is granted on a per-application basis, but it's also revoked on a per-application basis."

### Application cleanup
Problem: "Applications are hard to clean up."

### Isolation
Problem: "Shared services introduce undesirable dependencies between colocated applications."

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
