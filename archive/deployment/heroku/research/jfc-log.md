# Heroku notes

Jean Cochrane | Lead developer | July 2019

## Answers to questions

- **How much of a conceptual leap is it from our current dev/deployment practices to Heroku? What would it take to convert an app?**

The biggest conceptual leap for me was having to containerize the application. Theoretically Heroku should allow us to deploy non-containerized applications if we use buildpacks (which are basically container images for common application types that Heroku manages) but for most uses I suspect we'll have to use Docker instead. As an example, the Django buildpack doesn't come with GeoDjango support, so I wasn't able to test the buildpack for my R&D.

Depending on how you look at it, this could be either an advantage or a disadvantage of the platform. We've been talking about wanting to invest more in containers, and if we do that, Heroku will make a lot of sense. If, however, we decide we want to continue developing with local dependency management, then Heroku likely wouldn't be a great fit.

Outside of app containerization, the Heroku platform feels like a natural extension of our practices. Heroku Pipelines provide you with review apps that get built on every PR, as well as a staging and production environment, both of which can be triggered by GitHub pushes (and which can be configured to wait until tests pass before building). The workflow feels a lot like Netlify, if Netlify were deploying containers for us. The interface is about a thousand times more friendly than AWS, too.

- **What is monitoring like? Do we get shell access to services, or do we have to use a UI console? If we get shell access, how are permissions configured?**

Heroku gives you shell access to services through the Heroku CLI. Authentication is managed by Heroku for the CLI: When you run `heroku login`, the CLI opens up a browser and asks you to authenticate with Heroku. Then, you get shell access to any services for which you're a Collaborator on Heroku.

You can use `heroku run` to run one-off commands against running services -- e.g. here's how I opened up a shell to create a superuser for my app:

```bash
heroku run --app just-spaces bash
```

Heroku Postgres exposes [its own CLI subcommand](https://devcenter.heroku.com/articles/heroku-postgresql#using-the-cli) that you can use to interact with the database. Here's how you open up a `psql` session:

```bash
heroku pg:psql
```

Beyond shell access, you can also monitor service health and behavior through the Heroku console. Each app (like review, staging, or production) has a `metrics` dashboard showing memory usage, response time, and throughput, as well as the amount of load on the dynos (the Heroku containers).

- **How do the CI/CD features work? Do we indeed get fully ephemeral applications out of the box for PR/staging/production? How much extra does this cost?**

We do indeed get fully ephemeral applications out of the box, but at a cost. On Heroku you pay per usage, so the more dynos you run, the more you have to pay. In practice, however, Heroku has a free tier for both apps and Postgres that met my needs perfectly fine for review and staging apps.

The CI costs $10/mo, but I found that you don't actually need it in order to tie CI to CD -- you can configure a Heroku app to only deploy once tests have passed, even if those tests are run by an external provider.

- **What is the integration like between Heroku Runtime and Heroku Postgres? Can apps easily communicate with a protected database as in a VPC, or does it require lots of custom configuration?**

The integration is really smooth, and is by and large abstracted away from the developer. You can set a Heroku config file in your repo to specify that your app requires a database, and then when Heroku spins up review apps it'll automatically create and connect a database, updating your app's config variables to provide the database connection URL. (For staging and production apps you have to create the Postgres database manually, but this is as simple as clicking one button in the console and choosing your database size.)

The main downside of Heroku Postgres is that the app and the database don't live in the same VPC. Instead, the database is exposed to the public Internet, which is how your application authenticates with it (and how you authenticate with it over the CLI). There's nothing strictly insecure about this method, but database administrators generally advise you not to expose your database to the public Internet, because it means that if there's a security flaw in the way the database is configured then attackers can get direct access to your database without having to crack into your application first.

Another downside is that Heroku Postgres is pretty expensive. There's a "hobby" tier that gives you 10,000 rows for free, and you can bump it up to 1,000,000 rows for $9/mo, but these databases are colocated with other customer's databases and don't come with uptime guarantees or advanced monitoring. (You can also `psql` into your database and see other people's databases, which is kind of creepy! I poked around and it seems like they've configured the permissions pretty well, i.e. you can't access any other users' data, but it just goes to show that the cheapo tier is basically just creating a database inside a big shared Postgres cluster.) The cheapest option that isn't colocated is $50/mo. This is actually pretty comparable with AWS RDS pricing, but it's a lot more expensive than our current practice of colocating our Postgres and app installs on the same EC2 instance.

- **What is secrets management like? Can we use Blackbox? Can we download secrets from a remote source like S3? Or do we have to use a custom Heroku solution?**

Like Travis CI, Heroku lets you configure secret environment variables for each app through its console (or its CLI). Those environment variables then get threaded into the application at build time and at runtime. Public environment variables can be configured in the Heroku configuration files that you keep in your repo.

This sort of paradigm works a lot better with containerized applications, where you can define the environment through an `.env` file or `environment` attribute in a Docker Compose file and then pass those into the container. I could see a simple secrets management solution where we have an encrypted `.env` file for local development (or just download it from S3), and then for review/staging/production we configure secret environment variables in the Heroku console.

- **How is networking configured? Can we point DNS to a Heroku load balancer, as with Netlify? Or do we need to do more complicated DNS delegation?**

DNS delegation is a little bit different than Netlify because Heroku doesn't have a full DNS service the way that Netlify does. On Heroku, if you want to put your app behind a custom domain, you have to create an `ALIAS` or `CNAME` record in your DNS provider that delegates DNS to a Heroku hostname.

This pattern works perfectly fine for subdomains, but for root domains it's a little tricky because our domain registrar of choice (NameCheap) doesn't currently offer `ALIAS` or `ANAME` records for root domains. To get custom root domains to work with Heroku, we'd need to use a different domain registrar. (Luckily, this is a pretty common feature these days, and I'm surprised NameCheap doesn't offer it.)

- **What is dyno performance like at the pricing levels that are comparable to our current practices (two small EC2 instances, one for staging and one for production)?**

Dynos are comparably priced to EC2 instances: there's a free tier that works nicely for review and staging apps, a super-cheap "hobby" version that's $7/mo but doesn't come with horizontal scaling or long-term metrics, and then a "standard" version that's $25/mo. The hobby and standard version both come with 512GB of RAM, which is basically half of a t3.micro EC2 instance. Beyond "standard" you can pay a lot more for more RAM, but those seem out of our price range.

The biggest difference between EC2 and Heroku pricing is that an EC2 instance can run a bunch of different processes while a dyno can only run one (since it's basically a container). In practice this means that Heroku will be more expensive than EC2 since we'll need to pay for at least two dynos (production application and production Postgres) for any given application.

However, the $7/mo offering seems really appealing to me, and for low-traffic sites I can't figure out a reason why it wouldn't work. In this case, Heroku would probably be cheaper than EC2. I'd love for someone else to check my reasoning on this.

For more on dyno pricing, see the [pricing page](https://www.heroku.com/pricing).

## Feature parity

These are the tasks that I completed to ensure feature parity with Just Spaces:

- [x] Get staging app up and running with database, Django app, and staging user
- [x] Get a review app up and running with database, Django app, and staging user
- [x] Make sure that new PRs automatically generate review apps and tear them down when closed
- [x] Get production app up and running with database, Django app, and staging user
- [x] Set up the production app with a custom domain (heroku.jeancochrane.com) and SSL support

You can see my test app at https://heroku.jeancochrane.com!

## Pro/cons with other options

Currently, the main alternative to Heroku is our stack as documented in `deploy-a-site`: EC2 instances with Postgres and the application installed, deployed using our zero-downtime deployment framework.

In general, I think Heroku would be a good choice in cases where:

- We're able to fully containerize the application, and the dev team is comfortable with Docker
- The client has agreed to pay for hosting somewhere between $100-200/mo
- The app is a Django service with a Postgres database (it should be possible to deploy e.g. Solr on Heroku, but we haven't tested it yet)

### Pros

- Fully ephemeral applications that get recreated on every push
- Automatically built review apps for PR review
- Easy horizontal scaling during heavy load by adding more dynos
- Containerized production environment can align dev and prod for containerized apps
- UI is way easier to use than AWS

### Cons

- Requires that the dev team be comfortable with Docker and be able to fully containerize an application
- Still haven't proved out deployment of other services like Solr or Celery in addition to the app and the database
- Custom root domains may not work with all domain registrars
- More expensive than AWS, particularly Heroku Postgres

## Next steps

If we want to consider pursuing Heroku, I think a good next step would be trying to deploy a slightly more complicated application, e.g. one that uses Solr for searching and executes background tasks with Celery or a similar service. I also think a good next step would be to write up some documentation for how to deploy apps on Heroku; the Heroku docs are very thorough but there are a lot of them, and I think Heroku would benefit from the `deploy-a-site` treatment. At this point if we were to decide to continue pursuing Heroku I would feel comfortable piloting it on a client project.

## Lunch&Learn outline

- Talk about the pain points we face in deployments
    - We spend more time than we would like to doing unpleasant server maintenance
    - Our zero-downtime deployment strategy is mature but brittle, which indicates to us that perhaps we're overengineering our solution
    - We would like to containerize our production apps, but we don't know where to start, and we've had bad experiences with trying to orchestrate containers on AWS ECS and on bare EC2 instances
- Show how to containerize app with Heroku configs
    - Show code changes
    - Download, install, and run app
- Preview review apps
    - Make a small change to the codebase
    - Push it, create new PR
    - While review app builds, show the Heroku interface
- Tour of Heroku interface
- Demo Heroku CLI tools
    - `heroku logs`
    - `heroku run -a just-spaces bash`
- Talk at a high level about alternatives to Heroku
- Questions?

## Raw notes

These notes are pretty raw, and just represent things I wanted to keep for later. I present them for posterity but I don't necessarily recommend you read them.

- Heroku CI costs $10/month/pipeline. (Prorated to the second, so if you cancel
  your CI you don't have to pay for it.) On top of this, you have to pay for dynos
  and add-ons, which are prorated by the second.
    - CI is optional; you can configure the GitHub app to only run deployments
      after tests from an external provider (like Travis CI) pass

- Python buildpacks worked great, but couldn't access GDAL for GeoDjango.
  This means that our builds will have to be containerized if we want to use
  GeoDjango.

- Some web process notes:
    - Have to call the process `web`
    - Have to bind to $PORT

- CLI is really nice!
    - e.g. Web-portal based login flow

- Logging is not always straightforward, especially in Heroku CI
    - e.g. Kalil couldn't get dyno to "connect"; turns out the dyno just
      wasn't running, because he hadn't named in `web`!
    - e.g. My config file had messed up indentation, but instead of telling me
      that it was malformed it just told me that I didn't have a `build` step
      (which I had)
    - However, `heroku logs` is really nice, and once I got the applications up and
      running I felt like I had great logs

- SSH tunneling is easy with buildpacks, but hard with Docker. See:
  https://devcenter.heroku.com/articles/exec#using-with-docker Hoewver, `heroku run bash`
  should work for most workflows; we use tunneling pretty sparingly for apps.

- I got random failures during CI with no output except "a fatal error occurred" :(
  - Currently not possible to test container builds!
  - But `heroku ci:debug` is really cool!

- The `setup` portion of the `heroku.yml` manifest file will only provision
  add-ons etc. if you use a beta CLI plugin

- Can't "promote" container builds from staging to production; instead, have to
  set up branch deploys (this is how we do things now)

- DNS for custom domains requires an ALIAS or CNAME record. This is fine for
  subdomains, but for root domains we can't do this with NameCheap; we'd need
  to use another registrar (like AWS) that supports ALIAS or ANAME records
  for root domains.

- SSL for custom domains requires paid dynos (this only matters if we want to
  use custom staging URLs).

- Why won't new production app recognize heroku.yml?
    - You have to run `heroku -a app-name stack:set container`

# Divio notes

Divio is a really nifty platform, but after a couple hours of trying to get LISC CNDA
deployed on it, I can already tell that it's not right for our workflow.
I recommend abandoning this R&D.

The biggest reasons that Divio won't work with our stack are:

1. **Requires strict adherence to their repository structure.** Divio doesn't require any configuration files to deploy, which is nice, but the lack of configuration options also means that you're restricted by their repository requirements. Certain files and folders _have_ to exist in certain places, and there's no clear way to configure them to live elsewhere. Many of our repositories could be refactored to match these requirements, but many of them (like https://github.com/datamade/lisc-cnda) would require major overhauls. Some required patterns that were dealbreakers for LISC included:
    - Must have a `requirements.in` file at the root of the repo
    - Must have the Django project directory at the root of the repo
    - Requires the Django Dockerfile live at the root of the repo
2. **Gaps in documentation.** This might be because the service is changing rapidly, but there were some basic features that I couldn't find documentation for. For example, I tried to set up a "No platform" project (no Django stack, just a minimal Docker setup) but couldn't find anything on how to structure my project -- pretty important, because without a Django scaffold, I need to somehow be able to tell the service how to serve my app.
3. **Unintuitive GitHub integration.** Divio [does integrate with GitHub](http://docs.divio.com/en/latest/how-to/resources-configure-git.html), but in practice, the integration is cumbersome to use. Divio can't actually integrate with an external Git remote unless the `master` branch on the remote _only contains a README_ (a limitation which is lightly documented [here](http://docs.divio.com/en/latest/how-to/resources-configure-git.html#the-master-branch-must-exist-and-only-include-a-single-readme-file-in-order-to-create-a-new-project)). This limitation exists because Divio needs to commit a specific repo structure to your remote (see point 1 above). Because of this limitation, the only way to get my project to sync with the GitHub repo was to remove all the files from `master`, push it up, sync with Divio, and then revert the previous commit. This is pretty strenuous for what should be a simple task, and it's not really documented to my satisfaction.
4. **Unclear deployment logs.** In trying (and failing) to get my app with a slightly non-standard structure to deploy, the only deploy logs I saw were empty except for the output `starting docker build`. Most likely this is because my project had the wrong structure, but I need the build logs to be able to know if this is true.
5. **Not much of a community online.** I couldn't find any support to help debug except for official Divio docs (which, as I mentioned earlier, were sometimes outdated). This is a bad sign for a deployment provider.

Overall, I still think there's a lot of promise for a service like Divio. However, I wouldn't recommend we start using them just yet. I would be interested in revisiting Divio in a year or two, or if someone in our network starts using them extensively.
