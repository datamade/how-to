# Streaming replication

Interested in copying changes from one Postgres cluster to another **in real time**? This is the guide for you. You have two options:

1. [Stream an entire read-only database cluster](#stream-an-entire-read-only-database-cluster)
2. [Stream a subset of tables using logical replication](#stream-a-subset-of-tables-using-logical-replication)

# Stream an entire read-only database cluster

*Note: Commands prefixed by `$` represent work done on the sending server ("primary"), while commands prefixed by `¥` represent work done on the replicant server ("replicant").*

These steps assume that you have a primary database server up and running, and a replicant database server that is ready to go and initialized but empty.

Since we're going to overwrite the replicant database using the primary, **make sure that your replicant configuration files live in a separate directory from your data**. You can set this up by modifying the `data_dir` attribute in `postgresql.conf` to point to a separate directory where the data will live.

### 1. Create a replication user

```bash
# Create a new replication user
$ psql -U postgres -c "CREATE USER replicant REPLICATION LOGIN ENCRYPTED PASSWORD 'thepassword';"
```

Our standard Postgres setup allows blanket permissions for users with a local connection. If your setup is different, make sure to give the new replicant user access to the primary:

```
# Append this to the primary pg_hba.conf file
#
# TYPE  DATABASE        USER            ADDRESS                 METHOD
host    <dbname>        replicant       127.0.0.1/32            md5
```

### 2. Tweak settings on the primary to allow replication

```bash
# Append this to the postgresql.conf file,
# or uncomment the relevant attributes if they already exist
wal_level = hot_standby  # for 9.6+, this should be 'replica'
max_wal_senders = 3
wal_keep_segments = 8
max_wal_size = 1GB  # default
min_wal_size = 80MB  # default
```

Note from [the blog post where I cribbed these settings](http://www.rassoc.com/gregr/weblog/2013/02/16/zero-to-postgresql-streaming-replication-in-10-mins/):

> We’re configuring 8 WAL segments here; each is 16MB. If you expect your database to have more than 128MB of changes in the time it will take to make a copy of it across the network to your slave, or in the time you expect your slave to be down for maintenance or something, then consider increasing those values.

```bash
# Restart postgres
$ sudo service postgresql restart
```

### 3. Tweak settings on the replicant

These settings should be basically identical to the primary, with the notable addition of the `hot_standby` attribute.

```bash
# Append this to the postgresql.conf file,
# or uncomment the relevant attributes if they already exist
wal_level = hot_standby  # for 9.6+, this should be 'replica'
hot_standby = on
max_wal_senders = 3
max_wal_size = 1GB  #default
min_wal_size = 80MB  #default
```

Postgres will need to restart for these changes to take effect. Instead of restarting now, however, we can just turn it off, since we're going to be editing it now. **Stop Postgres** in whatever way you do it on your local machine.

### 4. Create an SSH tunnel to the primary

Follow [Hannah's excellent guide](https://github.com/datamade/how-to/blob/master/postgres/Interacting-with-a-remote-database.md) to tunnel into the primary.

In brief:

```bash
# Create the tunnel
¥ ssh -L 9000:localhost:5432 ubuntu@<hostname.ip.address>
```

### 5. Copy the primary to the replicant

For the initial copy, we'll use the [`pg_basebackup`](https://www.postgresql.org/docs/current/static/app-pgbasebackup.html) tool.

```bash
# Something isn't right with this command; not working
¥ pg_basebackup -h localhost -p 9000 -D /path/to/replicant/database -U replicant -v -P
```

### 6. Create a recovery.conf file on the replicant

```bash
¥ cat > /var/lib/postgresql/9.2/main/recovery.conf <<- EOF
  standby_mode = 'on'
  primary_conninfo = 'host=localhost port=9000 user=replicant password=thepassword'
  trigger_file = '/tmp/postgresql.trigger'
EOF
```

### 7. Start streaming

To begin streaming data, start Postgres on the replicant:

```bash
# You can replace this with a different command if you don't use pg_ctl
¥ pg_ctl start -D /path/to/replicant/configs

# You should see a bunch of logs confirming that it worked:
LOG:  database system was interrupted; last known up at 2017-03-13 13:26:30 CDT
LOG:  entering standby mode
LOG:  started streaming WAL from primary at 0/2000000 on timeline 1
LOG:  redo starts at 0/2000028
LOG:  consistent recovery state reached at 0/20000F8
LOG:  database system is ready to accept read only connections
```

You can test that the streaming is working by creating a new DB on the primary and verifying that it exists on the replicant:

```bash
# Create a DB on the primary
$ createdb -U postgres -O postgres test_replication

# Switch to the replicant, and view available databases
¥ psql -U postgres -c "\l"
```

## Further reading

### How-to guides

[Zero to PostgreSQL streaming replication in 10 mins](http://www.rassoc.com/gregr/weblog/2013/02/16/zero-to-postgresql-streaming-replication-in-10-mins/) - I cribbed a lot of the settings from this guide. Uses Postgres 9.2, so it's not fully up-to-date, but the explanations are nice and clear.

[How to Set Up a Read-Only PostgreSQL Slave Server for Data Analytics](http://beekeeperdata.com/posts/2016/11/09/read-only-postgres-slave.html) - Goes into more thorough detail than the last blog post, and covers Postgres 9.5/9.6 (which we use these days).

### Postgres official docs

[Log-Shipping Standby Servers](https://www.postgresql.org/docs/9.6/static/warm-standby.html) - Detailed explanations of how to configure a standby server, including streaming replication.

[Hot Standby](https://www.postgresql.org/docs/current/static/hot-standby.html) - More information on the concept/execution of "hot standby," the read-only, archival database state that powers this guide.

# Stream a subset of tables using logical replication

[**Logical Decoding**](https://www.postgresql.org/docs/9.4/static/logicaldecoding-explanation.html) is a nifty feature built into Postgres 9.4+ that can export all changes to a database's structure without requiring any knowledge of its state. The information it conveys is similar to a migration: after an update occurs, Postgres can extract changes from the write-ahead log that communicate changes like "a row got added to the table FOO with values (BAR, BAZ)", which you can then use to update a secondary database.

**Logical replication** is a smart way of using logical decoding to continuously copy a subset of tables in a database cluster. Instead of streaming binary information about an entire cluster ([as we did above](#stream-an-entire-read-only-database-cluster)), we can use logical decoding to filter for only the tables that we care about. This allows us to read and write to other databases/tables in the cluster without disrupting the stream that we're receiving from the master.

We'll implement logical replication using the Postgres plugin [pglogical](https://2ndquadrant.com/en/resources/pglogical/), built by the talented folks over at 2ndQuadrant. What follows is a pretty thin wrapper on [their documentation](https://2ndquadrant.com/en/resources/pglogical/pglogical-docs/), adding and subtracting a few steps based on things that didn't work for me or weren't well-explained in the docs. If anything is unclear here, try referring back to the official docs before jumping into Google to make sure I didn't miss anything.

### A note about pglogical lingo

pglogical uses a special set of terminology to talk about database structure. In particular, take note of the following keywords:

- **Nodes** are PostgreSQL database clusters. When two clusters communicate with one another, we'll refer to them as "nodes".
- Nodes can be **providers** or **subscribers**. Providers supply information about changes to their databases; subscribers receive that information and copy it.
- A **Replication Set** is a collection of tables or databases that you're interested in copying. It's the subset of the provider that will be copied to the subscriber.

### 1. Preliminary setup

Before starting to set up logical replication, make sure your project meets some baseline requirements:

1. Providers and subscribers must run the **same version of Postgres, 9.4 or higher** (2ndQuadrant claims there's some amount of cross-compatibility, but it seriously messed up my attempts to set up replication).
2. All tables that you want to stream need to have a **primary key or replica identity** to allow Postgres to extract precise changes.
3. If you're trying to stream to an existing set of tables, the **names and schemas must match exactly** between provider and subscriber. We'll move forward assuming that you've created the database on your subscriber but haven't created matching tables yet; if you already have the tables, double-check to make sure that the names and schemas match.

2ndQuadrant has a longer and more extensive list of requirements/limitations on [Section 4 of their docs page](https://2ndquadrant.com/en/resources/pglogical/pglogical-docs/). Give that a scan to verify that everything looks good.

### 2. Installation

To stream changes, the pglogical extension needs to be activated in both the provider and the subscriber clusters. This means that you'll have to install it on both machines.

2ndQuadrant hosts pglogical packages on both APT and YUM. Linux users can follow [their detailed instructions](https://2ndquadrant.com/en/resources/pglogical/pglogical-installation-instructions/) for downloading from the package manager of your choosing.

Since there are currently no Homebrew formulas for pglogical, macOS users should build the package from source:

1. Run `pg_config` and confirm that your Postgres environmental variables point to the correct installation location. (This should be fine if you installed Postgres with Homebrew.)
2. Clone the most recent version of the source code [off of GitHub](https://github.com/2ndQuadrant/pglogical), or wget and decompress the tarball from [the 2ndQuadrant package server.](http://packages.2ndquadrant.com/pglogical/tarballs/) Navigate to the repo.
3. Run `make` to compile the code, and then run `make install` to install it in the appropriate directories as specified by your PG config.

### 3. Set up the extension

Start by editing the `postgresql.conf` files for both your provider and subscriber clusters to allow them to import pglogical. (If you're not sure where these files live, you can query your databases with `SHOW config_file` to get the paths.) In both clusters, find the following variables and uncomment/edit them accordingly:

```
wal_level = logical
max_worker_processes = 10
max_replication_slots = 10
max_wal_senders = 10
shared_preload_libraries = 'pglogical'
```

(For the `worker_processes`, `replication_slots`, and `wal_senders` attributes, the docs recommend assigning an integer equivalent to the number of nodes that you want to send. This is probably fine, but tune accordingly if you have other replication needs.)

Next, restart postgres however you do that (`brew services restart postgresql`, `sudo service postgresql restart`, `pg_ctl restart -D path/to/data/dir`) to get these changes to take effect.

If you haven't already made a database on your subscriber to match your provider, do so now:

```
createdb <db>
```

Finally, install the pglogical extension on both clusters:

```
CREATE EXTENSION pglogical;
```

### 4. Start a subscription

We'll begin setting up our subscription by creating a **provider node** on the server that we want to track. Open up the desired database and run the following SQL query, replacing everything in < braces > with custom variables to match your project:

```
# The dsn tells pglogical how to connect to the database. We usually connect
# via localhost, on port 5432, with the postgres superuser.
SELECT pglogical.create_node(
    node_name := '<id_for_provider_node>',
    dsn := 'host=localhost port=5432 user=postgres dbname=<db>'
);
```

Next, define a **replication set** on the provider server to specify the tables that you want to pull out information from. We'll tell it to track all public tables and sequences, but if you want to filter for a smaller subset you can look at [Section 2.4 Replication Sets](https://2ndquadrant.com/en/resources/pglogical/pglogical-docs/) in the docs.

```
# Add all public tables and sequences in the current database
SELECT pglogical.replication_set_add_all_tables('default', schema_names:= ARRAY['public'], synchronize_data := true);
SELECT pglogical.replication_set_add_all_sequences('default', schema_names:= ARRAY['public'], synchronize_data := true);
```

(If any of your requested tables don't have primary keys/replica identities, pglogical will throw an angry error here. Create primary keys if you need to, or specify which columns to use for the replica identity.)

Let's move over to the subscriber now. We have to define a node again on this cluster:

```
# Same deal as above – tell pglogical how to connect to this cluster
SELECT pglogical.create_node(
    node_name := '<id_for_subscriber_node>',
    dsn := 'host=localhost port=5432 dbname=<db> user=postgres'
);
```

Once that's done, we're ready to start the subscription! We define subscriptions on the subscriber node by telling it how to connect to the provider, so navigate over to your subscriber.

Remember that pglogical needs the **table names and schemas to match exactly** in order to begin a subscription. There are two ways to accomplish this: either you can tell it to sync the tables when the subscription initializes, or you can manually create the tables yourself with the appropriate schema. I didn't have much success with the automatic sync, since I had to work with a server/local machine that had different major versions of Postgres, but according to a few different sources this should work for you if that's the route you want to go:

```
# I set up an SSH tunnel to connect port 9000 on the subscriber to port 5432 on the provider. You can do it that way,
# or provide the host/port/user/password manually if Postgres is open to the Internet on your server.
SELECT pglogical.create_subscription(
    subscription_name := '<id_for_the_subscription>',
    provider_dsn := 'host=localhost port=9000 dbname=<db> user=postgres',
    synchronize_structure := true,
    synchronize_data := true
);
```

If this works but doesn't immediatley update the tables, some users have suggested calling `pglogical.alter_subscription_resynchronize_table` for each table. You may also have to restart Postgres for the subscription to initialize. If all else fails, you can also just create the tables by hand with matching schema.

Note that the error messages aren't super descriptive here. I was getting the error:

```
subscriber test_subscription initialization failed during nonrecoverable step (s), please try the setup again
```

as well as an error about having the wrong version of `pg_dump` (which pglogical uses to sync for the first time). I solved both of them by manually creating the tables. If you choose to manually restore/create the tables, you can run the `create_subscription` method without synchronization:

```
SELECT pglogical.create_subscription(
    subscription_name := '<id_for_the_subscription>',
    provider_dsn := 'host=localhost port=9000 dbname=<db> user=postgres',
);
```

Now your subscription should be running. Great job! Confirm that you're streaming changes by moving things around on the provider and confirming that the changes apply to the subscriber.

## Further reading

[The pglogical docs](https://2ndquadrant.com/en/resources/pglogical/pglogical-docs/) are not super extensive, but useful enough.

I also found [this GitHub issue](https://github.com/2ndQuadrant/pglogical/issues/41) useful for helping me debug esoteric errors.
