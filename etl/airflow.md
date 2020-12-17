# 🌀 ETL Management with Airflow

### Contents

- [Why Airflow?](#why-airflow)
- [Basic concepts](#basic-concepts)
  - DAG
  - Task
  - Operator
  - Pipeline
- [Recommended default settings](#recommended-default-settings)
- [Best practices for DAGs](#best-practices-for-dags)
  - Depedency management
  - Scheduling
- [Deploying Airflow](#deploying-airflow)
- [Tips and Tricks](#tips-and-tricks)
  - Starting a Flask shell
  - Preventing worker refresh when debugging
  - Reloading plugin code
  - Setting `start_date`
  - Using the CLI

## Why Airflow?

Running jobs on a schedule is a common feature of data pipelines, such as
[DataMade’s legislative
scrapers](https://github.com/opencivicdata/scrapers-us-municipal/). The
traditional solution for scheduling tasks is
[cron](https://en.wikipedia.org/wiki/Cron). In fact, until 2020, it was [the
preferred
solution](https://github.com/datamade/scrapers-us-municipal/blob/c537c27dbd949cf6b838612325f087b2e3860252/scripts/la-metro-crontask)
at DataMade!

However, cron contributed to or made it more difficult to solve some tough
problems for our scrapers, including [scheduling
typos](https://github.com/datamade/scrapers-us-municipal/pull/50),
[colliding](https://github.com/datamade/scrapers-us-municipal/issues/38)
[scrapes](https://github.com/datamade/scrapers-us-municipal/issues/3), and
[indefinitely hung
processes](https://github.com/datamade/scrapers-us-municipal/issues/55). Beyond
bugs and developer experience, our usage of cron did not give our clients any
insight into whether scrapes had run, and to what outcome.

What we wanted was a framework that would allow us to define, manage, and
monitor our ETL jobs, and also expose an interface for interested parties to
follow along. We investigated three candidates:
[Airflow](https://airflow.apache.org/index.html),
[Luigi](https://github.com/spotify/luigi), and
[Rundeck](https://www.rundeck.com/open-source). Rundeck seemed optimized more
for server administration than data workflows, so we mostly considered Airflow
vs. Luigi.

[This article](https://towardsdatascience.com/data-pipelines-luigi-airflow-everything-you-need-to-know-18dc741449b7)
provides an excellent comparison of Airflow and Luigi. The important
distinctions for us were as follows:

1. Airflow supports scheduling tasks, while Luigi [purposefully omits this
functionality](https://luigi.readthedocs.io/en/stable/central_scheduler.html).
2. Luigi is a build tool. [Its units of
work](https://luigi.readthedocs.io/en/stable/tasks.html) are more Make-like in
that they are tightly coupled to output from their composite targets.
Conversely, Airflow operators run independently of one another, i.e., Airflow
feels more conceptually appropriate for scheduling tasks that don’t necessarily
create file-like artifacts, like scraping data.
3. Airflow has eclipsed Luigi in
popularity and maintenance resources, as measured by forks, stars, and watchers,
and commits, respectively.

Based on these impressions, and [an initial proof of
concept](https://github.com/datamade/scrapers-airflow), we selected Airflow as
our tool of choice for ETL management. Our first Airflow instance is the LA
Metro Dashboard, which has been open sourced
[here](https://github.com/datamade/la-metro-dashboard).

## Basic concepts

Airflow is a framework that relies on several key concepts. For a tutorial that
guides you through a summary of these concepts in Airflow’s words, go to
[https://airflow.apache.org/docs/stable/tutorial.html#example-pipeline-definition](https://airflow.apache.org/docs/stable/tutorial.html#example-pipeline-definition).
Below are listed the most important Airflow concepts based on our work with
Airflow thus far.

### DAG (directed acyclic graph)

A DAG is a way of visualizing the way Airflow works. It emphasizes that Airflow
moves through tasks in a particular order without automatically repeating those
tasks, and includes information about tasks’ dependencies on each other.

- Airflow’s description:
- [https://airflow.apache.org/docs/stable/concepts.html#dags](https://airflow.apache.org/docs/stable/concepts.html#dags)
- A DAG run is an instance of a DAG.

### Task

A task is a single function or command to run. At the bare minimum,
instantiating a task requires a `task_id`, `dag`, and the command argument for
the particular operator being used.

For example, the `bash_operator` has a `command` argument, whereas the
`python_operator` has a `python_callable` argument. A task run is an instance
of a task.

### Operator

Airflow is really powerful in part because it can run commands for any part of
your app that you can write in the most convenient language for that task [not
sure about wording here]. For example, you can write a scraping script in Bash
and run it with the `bash_operator`, run a Python command using the
`python_operator`, and then run a database command using the `postgres_operator`
-- all in the same DAG!

There are also operators that handle control flow and other kinds of tasks. For
a full list, see
[https://airflow.apache.org/docs/stable/_api/airflow/operators/index.html](https://airflow.apache.org/docs/stable/_api/airflow/operators/index.html)

### Pipeline

A configuration file for a DAG. There are five parts to a pipeline, and they
should be in this order:

1. **Imports and Operators:** The first part of writing a pipeline the same as
most files in an app; you start by importing any modules you will need.
Depending on the kinds of tasks you will need to run in your DAG, you will also
need to import different operators.

2. **Default arguments:** After importing your operators and other dependencies,
define a dictionary containing all the arguments that the tasks in your DAG will
have in common. A few often-used ones to know about:

    - `start_date`: the date that the DAG should begin running tasks for. For
    example, if you intend to run a task to run a scraping task daily starting
    on January 1, 2020, the first DAG run will happen on January 2 in order to
    gather all of the information that may have been added to the source
    throughout the day of January 1.
    - `end_date`: the last date for which a DAG should run.
    - `execution_timeout`: How long the task should continue to run before
    giving up. For example, if you need a DAG to run every 3 hours, you may want
    to make sure the previous DAG run is no longer running. Setting an
    `execution_timeout` of, for example, 2 hours and 55 minutes, would force the
    first DAG run to stop in time for the next DAG run to begin without
    overlapping.
    - `retries`: If a DAG fails, the number of times it should try to run again.

3. **Instantiate a DAG:** The next step is to instantiate a DAG. Here are a
couple of important arguments to know:

    - `dag_id`: a string that gives the DAG a name. This is the name that shows
    up in the Airflow dashboard for this DAG.
    - `schedule_interval`: the amount of time that should elapse between DAG
    runs. This can be [a cron string](https://crontab.guru/), or you can use
    [one of Airflow’s presets](http://airflow.apache.org/docs/stable/dag-run.html#cron-presets)
    - `default_args`: set this equal to the dictionary defined in step 2. More
    info about [the Airflow DAG object](http://airflow.apache.org/docs/stable/_api/airflow/models/dag/index.html#module-airflow.models.dag)

4. **Tasks:** In the penultimate step of defining your pipeline, define out the
DAG’s tasks. Each task is an instance of one of Airflow’s operators, so look at
the documentation for that specific operator for the most detailed information
on how to define a task. Here’s the list of operators:
[https://airflow.apache.org/docs/stable/_api/airflow/operators/index.html](https://airflow.apache.org/docs/stable/_api/airflow/operators/index.html)

    Keep in mind that there are also operators that are focused on control flow
    that you might need to use in defining tasks. A couple common ones you might
    use:

    - Branch Operator: Allows you to run different tasks at different times or
    under different conditions
    - Dummy Operator: If you want to avoid running a task if a certain condition
    is true, you can use the Dummy Operator to run a fake task in place of the
    true one.

5. **Task ordering and dependencies:** The final part of the pipeline is task
ordering. Here, set the order that the tasks should run in and how they depend
on each other. The example code given on the Airflow docs is concise and
helpful:
[https://airflow.apache.org/docs/stable/tutorial.html#setting-up-dependencies](https://airflow.apache.org/docs/stable/tutorial.html#setting-up-dependencies)

## Recommended default settings

### All environments

```cfg
# Point Airflow at your Postgres database, rather than the SQLite default
sql_alchemy_conn = postgres://postgres@localhost:5432/${PG_DATABASE}
```

### Local `airflow.cfg`

```cfg
# Don't load example DAGs
load_examples = False

# Turn on authentication
authenticate = True

# Turn on role-based access control (Airflow's new model of authentication, with a separate UI)
rbac = True

# Don't catch up to old DAGs when restarting the process
catchup_by_default = False

# Increase interval between worker refreshes to give yourself time to debug
# See "Preventing worker refresh when debugging" in the section on debugging, below
worker_refresh_interval = 10000
```

We may not always want authentication and RBAC. I think that should probably be a project-by-project decision.

### Production `configs/airflow.production.cfg`

```cfg
# Store logs in /var/log intead of AIRFLOW_HOME
base_log_folder = /var/log/la-metro-dashboard/airflow
dag_processor_manager_log_location = /var/log/la-metro-dashboard/airflow/dag_processor_manager/dag_processor_manager.log

# Use a single node for task execution
executor = LocalExecutor

# Only two task instances should be able to run simultaneously
parallelism = 2

# The scheduler should only be able to run two task instances
dag_concurrency = 2

# Workers should only be able to run two task instances
worker_concurrency = 2

# Don't load example DAGs
load_examples = False

# Turn on authentication
authenticate = True

# Turn on role-based access control (Airflow's new model of authentication, with a separate UI)
rbac = True

# Don't catch up to old DAGs when restarting the process
catchup_by_default = False
```

Again, authentication and RBAC should be set project-by-project. The concurrency configs are super confusing and [the docs](https://airflow.apache.org/docs/stable/configurations-ref.html) don't really help so I think there's a lot of opportunity for better tuning in the future.

## Best practices for DAGs

### Dependency management

One of the pitfalls of our legacy scrapers was that our dependencies [were
tightly coupled with / constrained by the server
environment](https://github.com/datamade/scrapers-us-municipal/issues/40). We
also needed to solve the problem of how to run commands against remote
codebases. (Our cron jobs were simply co-located with app code they needed to
run their scrapes and subsequent ETL steps.)

For both of these reasons, we prefer to use Airflow’s
[DockerOperator](https://airflow.apache.org/docs/stable/_api/airflow/operators/docker_operator/index.html#airflow.operators.docker_operator.DockerOperator)
to run tasks. A more detailed discussion of how we arrived at this decision is
located [in this
issue](https://github.com/datamade/server-la-metro-dashboard/issues/1) (internal
link). See [the LA Metro Dashboard
documentation](https://github.com/datamade/la-metro-dashboard#application-dependencies)
for more information about how this strategy works in practice.

### Scheduling

Airflow provides a couple of ways to schedule DAGs. You can declare [a schedule
interval](https://airflow.apache.org/docs/stable/dag-run.html) as a cron or
“cron preset” expression, and you can write [custom branching
logic](https://airflow.apache.org/docs/stable/concepts.html#branching) to
perform certain tasks based on an exogenous variable, e.g., what time the DAG is
running.

The latter approach can be very attractive when you have a schedule interval
that cannot be expressed in cron syntax, as [it is not possible to declare
multiple schedule intervals](https://github.com/apache/airflow/issues/8649) for
a single DAG. However, it spreads scheduling concerns across different parts of
the code and precludes manually triggering DAGs, as the scheduling logic may not
yield the desired path.

We prefer to consolidate scheduling concerns and use only the schedule interval
to schedule DAG runs. We are [actively working on identifying a preferred
strategy](https://github.com/datamade/la-metro-dashboard/issues/59) for doing
this while minimizing repeat code and clever architecture.

## Deploying Airflow

In theory, Airflow should be easy to deploy on Heroku. There are a number of
guides for doing this online (like [this
one](https://medium.com/@damesavram/running-airflow-on-heroku-ed1d28f8013d)).
Most use Procfiles instead of the container stack, but our [docs for deploying
Django on Heroku using the container
stack](https://github.com/datamade/how-to/blob/master/heroku/deploy-a-django-app.md)
should be straightforward to adapt for a Flask app like Airflow.

However, our first production Airflow instance, the [LA Metro
Dashboard](https://github.com/datamade/la-metro-dashboard/), is deployed on AWS
EC2 via CodeDeploy using DataMade’s [legacy deployment
framework](https://github.com/datamade/deploy-a-site/). The primary reason we
had to fall back to our legacy framework is because **we needed a stable IP
address that we could safelist to access an external Solr instance**. Our
original plan was to expose our Solr instance publicly and enable
[SSL](https://lucene.apache.org/solr/guide/7_6/enabling-ssl.html) and [basic
authentication](https://lucene.apache.org/solr/guide/8_1/basic-authentication-plugin.html)
so that an Airflow instance on Heroku could communicate with it, but we were
unable to get either feature to work properly before we ran out of budget for
the task.

Since the IP address of a Heroku app can change without notice, Heroku is a bad
choice for an Airflow deployment that requires a static IP address. However,
this is currently the only hurdle to deploying Airflow on Heroku that we know
of, and we may be able to get around it with more research.

## Tips and Tricks

Since Airflow is a packaged Flask app, debugging it can be challenging. The
following is an evolving list of tricks that we have identified for debugging
Airflow.

### Starting a Flask shell

The following command will start a [Flask
shell](https://flask.palletsprojects.com/en/1.1.x/shell/) in the Airflow app:

``` bash
# This command assumes your Airflow service in docker-compose.yml is
# named “airflow”

docker-compose run --rm -e FLASK_APP=airflow.www.app airflow flask shell
```

### Preventing worker refresh when debugging

Airflow needs to periodically refresh its worker process in order to register
changes to DAGS, and by default it does this every 30 seconds. This can be
frustrating during debugging because refreshing the worker process will end a
running process and kick you out of a debugger that you’ve dropped into that
process.

To prevent reloading when debugging, you can temporarily set the
[`worker_refresh_interval`](https://github.com/apache/airflow/blob/11eb649d4acdbd3582fb0a77b5f5af3b75e2262c/airflow/config_templates/default_airflow.cfg#L430-L431)
config value to a very high number of seconds, like `10000`. Like all config
variables, this can also be set using an [environmental
variable](https://airflow.readthedocs.io/en/stable/howto/set-config.html#setting-configuration-options).

### Reloading plugin code

If you’re developing an [Airflow
plugin](https://airflow.apache.org/docs/stable/plugins.html), you’ll need to set
the
[`reload_on_plugin_change`](https://airflow.apache.org/docs/stable/configurations-ref.html#reload-on-plugin-change)
config to `True` if you want Airflow to watch for changes in your plugin code
and automatically reload. This config is only available in Airflow 1.10.11+ and
it’s set to `False` by default.

If you’re developing a plugin on Airflow &lt; 1.10.11, you’ll need to stop and
restart the web server and scheduler processes every time you want to view a
change to plugin code.

### Setting `start_date`

The `start_date` attribute of DAGs is a little bit challenging to get your head
around if your DAG doesn’t have a clear “first date” on which it needs to run.

The key thing to remember is that `start_date` should always be a static value.
You may find Airflow docs or examples that set a dynamic value, but [we’ve found
that static values behave more
consistently](https://github.com/datamade/la-metro-dashboard/issues/37#issuecomment-661112215).

For background on `start_date`, see the [Airflow
FAQ](http://airflow.apache.org/docs/stable/faq.html#what-s-the-deal-with-start-date).

### Using the CLI

Airflow includes an [extensive CLI for common
operations](https://airflow.apache.org/docs/stable/cli-ref). Some operations we
often use include:

- [`create_user`](https://airflow.apache.org/docs/stable/cli-ref#create_user) (Create a user for the web UI)
- [`delete_user`](https://airflow.apache.org/docs/stable/cli-ref#delete_user) (Delete a user for the web UI)
- [`webserver`](https://airflow.apache.org/docs/stable/cli-ref#webserver) (Start a web server instance)
- [`scheduler`](https://airflow.apache.org/docs/stable/cli-ref#scheduler) (Start a scheduler instance)

**Note that the `AIRFLOW_HOME` environment variable must always be set for CLI
commands to run.** It’s easy to forget this variable and receive an esoteric
error message, particularly on a server, since Airflow sets a default value for
`AIRFLOW_HOME` and may not report this to you.
