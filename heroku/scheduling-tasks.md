# Scheduling tasks on Heroku

Often when deploying a web app we want to run application code on a certain schedule:
compiling summary statistics, updating data in a database from a remote source, etc.
In the past we've used the software utility [cron](http://man7.org/linux/man-pages/man8/cron.8.html)
for this purpose, but cron is an unreliable choice for containerized platforms like
Heroku because it assumes that it can run continuously on a single dedicated machine.

There are three tiers of options for scheduling tasks on Heroku, in ascending
order of complexity:

1. If your scheduled tasks are **simple**, are robust to **occasional failures or
   double-queueing**, and need to run either **hourly, daily, or every 10 minutes**,
   use the [Heroku Scheduler add-on](#heroku-scheduler).

2. If your scheduled tasks are **complex**, require a **detailed, cron-like schedule
   for running**, and **do not require intricate sequencing**, use the
   [Cron to Go add-on](#cron-to-go).

3. If your scheduled tasks are **complex**, require a **detailed, cron-link schedule
   for running**, and **require intricate sequencing**, use a [dedicated Airflow
   instance](#airflow).

## Heroku Scheduler

The Heroku Scheduler is a free add-on supported by the Heroku core team that provides
simple task scheduling.

### Requirements

To use Heroku Scheduler, your tasks must be:

- **Robust to occasional failures or double-queuing**: The Heroku task scheduler
  does not guarantee a task will be executed, or that it will be executed exactly
  once. For this reason, your tasks should be idempotent and not mission-critical
  in order to use the Heroku Scheduler.

- **Can run either hourly, daily, or every ten minutes**: These are the only three
  schedules offered by the Heroku Scheduler.

If your tasks do not meet these requirements, see whether [Cron to Go](#cron-to-go)
is the right solution for you.

### Installation and setup

Setting up the Heroku scheduler is simple and Heroku provides [good documentation
for getting started](https://devcenter.heroku.com/articles/scheduler).

## Cron to Go

Cron to Go is a paid Heroku add-on that offers task scheduling at a higher
level of complexity than the Heroku Scheduler.

### Requirements

To use Cron to Go, your tasks should:

- **Be schedulable with the cron syntax**: Cron to Go allows you to schedule
  Heroku tasks using the cron execution syntax. If you can schedule your tasks
  with cron, Cron to Go is a good choice.

- **Not require intricate sequencing**: Like cron, Cron to Go only supports sequencing
  of tasks insofar as you can define the interval between tasks and set a timeout
  for each task. This method of sequencing is sometimes not fine-grained enough for
  complex tasks like ETL.

- **Support paying $10-20/month for task execution**: Unlike the Heroku Scheduler,
  Cron to Go is not free, although it is cheaper than running your own dedicated
  clock process on Heroku.

If your tasks do not meet these requirements, consider [running a dedicated Airflow
service](#airflow).

### Installation and setup

Cron to Go is relatively easy to set up, and the service provides [good docs for
getting started](https://devcenter.heroku.com/articles/crontogo).

Note that there are different tiers of pricing for Cron to Go with different levels
of features. We expect that most projects will be fine with the cheapest plan, but
make sure to [double-check the pricing plans](https://elements.heroku.com/addons/crontogo#pricing)
to confirm that your plan meets your needs. In particular, if you need notifications
for your tasks, you should choose the Silver plan over the Bronze plan.

## Airflow

[Apache Airflow](https://airflow.apache.org/) is an open source Flask app that
provides a task scheduling and execution service.

### Requirements

To use Airflow, you should:

- **Be willing and able to host your own task scheduler**: Unlike the Heroku Scheduler
  and Cron to Go, Airflow is a self-hosted service that will require dedicated Heroku
  dynos and somewhere between 10 and 20 dev hours to set up.

- **Require intricate task sequencing**: Airflow is only a good choice if your
  tasks require intricate sequencing, such as tasks that should only run in certain
  conditions or tasks that require direct output from other tasks.

- **Support paying $50/month for task execution**: Airflow requires two dynos to
  run, one for the web app and one for the worker process, which comes out to $50/month
  on our current pricing plan.

### Installation and setup

Follow the [Airflow documentation](https://airflow.apache.org/docs/stable/installation.html)
to install and get started. In addition, you should consult with a lead developer
for help on configuring and deploying the app.
