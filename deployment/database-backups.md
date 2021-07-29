# Database backups

Protection from data loss is an important consideration for any production app.
This document contains guidance for taking backups of your database for all
three deployment scenarios currently in play in the DataMade stack.

### Contents

- [Heroku Postgres](#heroku-postgres)
- [Amazon Relational Database Service (RDS)](#amazon-relational-database-service-rds)
- [Self-hosted PostgreSQL](#self-hosted-postgresql) (Legacy deployments)

## Heroku Postgres

Heroku offers a stellar hosted database service in [Heroku Postgres](https://devcenter.heroku.com/articles/heroku-postgresql).

Among other features, Heroku Postgres offers [automatic backups for Standard-*
and above plans](https://devcenter.heroku.com/articles/heroku-postgres-data-safety-and-continuous-protection).
This covers DataMade's production databases.

Nothing to configure here! See [the Heroku documentation](https://devcenter.heroku.com/articles/heroku-postgres-rollback)
for guidance on how to roll back to a previous version of your database.

## Amazon Relational Database Service (RDS)

Like Heroku Postgres, RDS [automatically creates backups for you](https://aws.amazon.com/rds/features/backup/).

_More to come if/when we officially adopt RDS._

## Self-hosted PostgreSQL

The simplest way to take a backup of a PostgreSQL database is to create a dump
file and then save that someplace else (like S3). Since sometimes you don't
want to save the dump file to the disk where the database is running (perhaps
it's very large and you have limited space), you can use the `aws` tool to pipe
the file directly to S3. 

Use this cron task to save a PostgreSQL database to an S3 bucket, making sure to
replace the `${DATABASE}` variable with the name of your database:

```bash
# /etc/cron.d/database-backups

# Back up the database at 4 AM GMT (11pm EST) every day.
0 4 * * * datamade (pg_dump -Fc -U postgres -d ${DATABASE} | /usr/bin/aws s3 cp - s3://datamade-postgresql-backups/${DATABASE}/$(date -d "today" +"\%Y\%m\%d\%H\%M").dump) && echo "backup $(date -d "today" +"\%Y\%m\%d\%H\%M").dump complete" >> /tmp/database-backups.log 2>&1
```

In addition, we need to make sure that the `datamade` user has permissions to
write to the log file as we've instructed it to in the command above (the log
file is called `/tmp/database-backups.log` in the command above, although you
can safely change this file name to be more specific to your project if you'd
like).

To make sure these permissions are set automatically, add the following code
block to the end of your `after_install.sh` script:

```bash
# after_install.sh

if [ "$DEPLOYMENT_GROUP_NAME" == "production" ]; then
  # Set the correct permissions for the cron job.
  chown root.root /etc/cron.d/database-backups
  chmod 644 /etc/cron.d/database-backups
  # Set the correct permissions for the backup log file.
  touch /tmp/database-backups.log
  chown datamade.www-data /tmp/database-backups.log
fi
```

For an example of this pattern in action, see the [Committee Oversight
project](https://github.com/datamade/committee-oversight/blob/master/scripts/committee-oversight-crontasks).

Note that the cron task above will create a full backup of your database every
day. Daily backups may be too frequent for your needs; often weekly backups are good enough for our clients. See https://crontab.guru/ for help adjusting the
frequency of your cron task.

If the `aws` tool isn't installed or if it's an older version, then you might
need to install a newer version in order to get the functionality that allows
you to pipe streamed data into the `s3` command. [Here are some
instructions](https://docs.aws.amazon.com/cli/latest/userguide/install-linux.html)
to get the most recent version.
