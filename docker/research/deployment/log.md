# Research log

## Objective

From https://github.com/datamade/how-to/issues/19:

> Identify a service to orchestrate the deployment of containers. In addition to orchestrating container deployment, this service should at minimum provide a web interface to container logs and provisioning container access by application. Ideally, it would also allow managing by access by user and centralize other key devops tasks, such as DNS and SSL management. We have identified two immediate candidate services: ECS and Heroku. We propose evaluating these services by standing up a containerized application in both and selecting the one we prefer. If we prefer ECS but desire further abstraction, we then propose trialing Fargate.

## Elements of deployment

1. Server provisioning
2. Image management
3. Container management
4. Logging
5. Secret management
6. Routing

## Amazon Elastic Container Service (ECS)

ECS is AWS's contribution to the container orchestration space. It works in
concert with several other AWS microservices to "deploy, manage, and scale
Docker containers."

In general, I followed the approach outlined here: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-cli-tutorial-ec2.html

My notes, as well as the modified `docker-compose.ecs.yml` and `ecs-params.yml`
files live [in a branch of `dedupe-service`](https://github.com/dedupeio/dedupe-service/pull/1487).

### Server provisioning

EC2.

I used the EC2 CLI, as recommended in the docs linked above.

Fargate would abstract needing to provision this away. I had the notion that
this was an expensive option, however there was [a significant reduction in price](https://aws.amazon.com/blogs/compute/aws-fargate-price-reduction-up-to-50/)
in early 2019. This doesn't make me any more able to decipher [AWS pricing pages](https://aws.amazon.com/fargate/pricing/),
but it's heartening just the same.

### Image management

Used ECR, since I didn't have access to the datamade DockerHub organization /
our image was private. DockerHub is an equally viable option.

### Container management

ECS.

ECS supports a modified `docker-compose.yml` syntax that allows you to skip
defining your services by hand. It also allows you to define AWS-specific
blocks, e.g., for logging integration with CloudWatch and secret management
in the parameter store.

### Logging

CloudWatch.

This was actually quite easy to set up, just needed to add a `logging` block
to each service:

```yaml
    logging:
      driver: awslogs
      options:
        awslogs-group: dedupe-service-ecs
        awslogs-region: us-east-1
        awslogs-stream-prefix: redis
```

### Secret management

Didn't set this up, but [seems possible via AWS Systems Manager Parameter Store](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/specifying-sensitive-data.html). Related documentation for the `ecs-params.yml` file needed to define secrets: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/cmd-ecs-cli-compose-ecsparams.html.

### Routing

ELB.

The documentation I was following suggested that I should be able to view my
application with the IP address and port, but that didn't seem to be the case.

TO-DO: Can I do this if I map my container to port 80 (the default when spinning
up EC2 instances)?

Instead, it's recommended to [use a load balancer to route web traffic](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-load-balancing.html).

When I tried to set up an ELB for my ECS-configured EC2 instance, the instance
was not available during configuration. This is where I put it down.

### Reflection

There are _a lot_ of microservices to configure here – and while some of that
configuration can be scripted, much of it takes place in far-flung corners of
the AWS console.

It also feels a bit off to transition to a service optimized for scaling, when
our real problem is managing single instances of an application. It makes things
like using a load balancer instead of a web server feel unnecessary.

That said, are some things to like:

- You can use familiar docker-compose syntax (with some exceptions).
- Wow, why aren't we using `ec2-cli` to provision our servers now?
- It's a breeze to set up logging.
- I like the idea of managing secrets in a central location, with access
controlled by IAM roles we already manage. I didn't realize this was something
AWS offered.
