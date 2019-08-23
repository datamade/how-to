# Research log

## Objective

From https://github.com/datamade/how-to/issues/19:

> Identify a service to orchestrate the deployment of containers. In addition to orchestrating container deployment, this service should at minimum provide a web interface to container logs and provisioning container access by application. Ideally, it would also allow managing by access by user and centralize other key devops tasks, such as DNS and SSL management. We have identified two immediate candidate services: ECS and Heroku. We propose evaluating these services by standing up a containerized application in both and selecting the one we prefer. If we prefer ECS but desire further abstraction, we then propose trialing Fargate.

## Services trialed

- [Amazon ECS](#amazon-elastic-container-service-ecs)
- [Heroku](#heroku)

## Elements of deployment

1. Server provisioning
2. Image management
3. Container orchestration
4. Logging
5. Secret management
6. Routing traffic

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

### Routing traffic

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

## Heroku

@jeancochrane explored Heroku-based deployments in May: https://github.com/datamade/how-to/issues/9#issuecomment-495775051.

Start there for useful context.

### Server provisioning

Heroku abstracts this away, however I only wanted to use the cheapo, single-dyno
tier. We will want to research, select, and document a sane default for most
applications. You can upgrade dynos in the Heroku UI, or via the CLI:
https://devcenter.heroku.com/articles/scaling#manual-scaling.

For advanced needs, e.g., Dedupe.io, Heroku offers enterprise accounts with
features like Private Spaces (with PCI, HIPAA, ISO, and SOC compliance) and
autoscaling. https://www.heroku.com/enterprise

### Image management

Heroku offers two options for containerized deployment: building your container
and publishing it to a registry, then releasing it to your dyno; or defining
your application in a yml file and building your application container/s from
bundled Dockerfile/s as part of each release: https://devcenter.heroku.com/categories/deploying-with-docker

I gave the former a try, but ultimately decided to pilot the latter, because
I preferred the expressive syntax, I liked that you could define addons, multiple
processes, and I wanted to run migrations as part of the release cycle, prior to
starting the app.

So the answer here is None, your container is built from your app's Dockerfile
on each deploy.

### Container orchestration

Heroku allows you to define an application, as well as add-on services and
pre-deployment steps, in a `heroku.yml` file. (@jeancochrane mentions that
this is also configurable in the UI!)

All told, the following took me about three hours to research, troubleshoot,
and deploy Dedupe.io on Heroku.

1. Create and verify a Heroku account.
2. Install and authenticate with the Heroku CLI. https://devcenter.heroku.com/articles/heroku-cli#download-and-install
3. Create a Heroku app.

   ```bash
   heroku apps:create dedupeio
   ```

4. Add the Postgres addon.

   N.b., while you can specify add-ons in your `heroku.yml` file, the `setup`
   block does not appear to fire as part of regular builds. Creating an
   application from a `setup` block, including the addition of add-ons,
   [is in beta](https://devcenter.heroku.com/articles/build-docker-images-heroku-yml#creating-your-app-from-setup).

   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

   Also note that the Postgres add-on injects a `DATABASE_URL` environmental
   variable into your container. You need to update your application settings
   to reference that variable, instead of a hard-coded URI.

5. Enter the `psql` shell and add extensions. I did this manually, however it
could also be automated with an `init_db` script in your application's language.

   ```bash
   # locally
   heroku pg:psql
   # in the heroku psql shell
   create extension if not exists pgcrypto;
   create extension if not exists intarray;
   ```

6. Write a heroku.yml file.

   ```yml
   # Setup doesn't actually run unless you create your app from setup
   # https://devcenter.heroku.com/articles/build-docker-images-heroku-yml#creating-your-app-from-setup
   setup:
     addons:
       - plan: heroku-postgresql
       - plan: heroku-redis

   # Specify the processes you want to run. These will be created in separate dynos.
   build:
     docker:
       web: Dockerfile
       worker: Dockerfile

   # Define scripts to run before your application/s start
   release:
     command:
       - alembic upgrade head || (python init_db.py && alembic upgrade head)
     image: web

   # Define commands to run application/s.
   run:
     # PORT is generated by Heroku
     web: python runserver.py --host 0.0.0.0 --port $PORT
     worker: python run_queue.py
   ```

7. Commit your changes and push them to Heroku.

   ```bash
   git add heroku.yml [updated_config.py updated_script.py ...]
   git commit -m "add heroku.yml"
   git push heroku your-branch:master
   ```

## Logging

Heroku exposes build and release logs in the UI. Application logs can be
viewed via the CLI, like `heroku logs --tail`.

## Secret management

Cribbed from @jeancochrane:

<blockquote>
<p>Like Travis CI, Heroku lets you configure secret environment variables for each app through its console (or its CLI). Those environment variables then get threaded into the application at build time and at runtime. Public environment variables can be configured in the Heroku configuration files that you keep in your repo.</p>

<p>This sort of paradigm works a lot better with containerized applications, where you can define the environment through an .env file or environment attribute in a Docker Compose file and then pass those into the container. I could see a simple secrets management solution where we have an encrypted .env file for local development (or just download it from S3), and then for review/staging/production we configure secret environment variables in the Heroku console.</p>
</blockquote>

## Routing traffic

Heroku provides a yourapp.herokuapp.com URL automatically. This on custom URLs
also cribbed from @jeancochrane:

<blockquote>
<p>On Heroku, if you want to put your app behind a custom domain, you have to create an ALIAS or CNAME record in your DNS provider that delegates DNS to a Heroku hostname.</p>

<p>This pattern works perfectly fine for subdomains, but for root domains it's a little tricky because our domain registrar of choice (NameCheap) doesn't currently offer ALIAS or ANAME records for root domains. To get custom root domains to work with Heroku, we'd need to use a different domain registrar. (Luckily, this is a pretty common feature these days, and I'm surprised NameCheap doesn't offer it.)</p>
</blockquote>

## Reflection

Overall, Heroku is several times easier than ECS, as well as even our current
deployment practices with EC2 and CodeDeploy.

It appears to play nicely with Travis, also: https://docs.travis-ci.com/user/deployment/heroku/

With that said, I didn't trial interactions between dynos, e.g., between an app
and worker process, so there may be some kinks to iron out there.

There also seems to be a price on convenience.

For our most complicated app (Dedupe.io), I think we'd need a $25/month 1x dyno
for the Dedupe.io frontend and a $50/month 2x dyno for the worker processes,
since they do some intense computing.

For most apps, though:

<blockquote>
Dynos are comparably priced to EC2 instances: there's a free tier that works nicely for review and staging apps, a super-cheap "hobby" version that's $7/mo but doesn't come with horizontal scaling or long-term metrics, and then a "standard" version that's $25/mo... However, the $7/mo offering seems really appealing to me, and for low-traffic sites I can't figure out a reason why it wouldn't work. In this case, Heroku would probably be cheaper than EC2.
</blockquote>

Add-ons are more persistently costly:

<blockquote>
<p>There's a "hobby" tier that gives you 10,000 rows for free, and you can bump it up to 1,000,000 rows for $9/mo, but these databases are colocated with other customer's databases and don't come with uptime guarantees or advanced monitoring... The cheapest option that isn't colocated is $50/mo. This is actually pretty comparable with AWS RDS pricing, but it's a lot more expensive than our current practice of colocating our Postgres and app installs on the same EC2 instance.</p>
</blockquote>

To really assess whether Heroku is more expensive, it would be very helpful
to know our current hosting costs, both for Dedupe.io and particular, and for
a run-of-the-mill application.

(Thanks to @jeancochrane for putting in the legwork here!)
