# Heroku CLI

You can use the Heroku CLI to do a lot of tasks, like shelling into your app, connecting to the database, or viewing your app's logs. We recommend that you learn to use this tool.

The Heroku docs are the best resource for any information about using the CLI. [Here's a good place to start](https://devcenter.heroku.com/articles/heroku-cli). Here's [a list of all of the CLI's commands](https://devcenter.heroku.com/articles/heroku-cli-commands).

Some useful commands:
- See the app's logs: `heroku logs -t -a <app_name>`
- Shell into the app: `heroku run bash -a <app_name>`
- Connect to the database via psql: `heroku pg:psql -a <app_name>`

## Database management
If you need to do anything related to your database, [check out this Heroku Postgres documentation](https://devcenter.heroku.com/articles/heroku-postgresql).
