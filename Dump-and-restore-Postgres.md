# Dump and restore a database

Occasionally, you need to dump a remote database and restore it locally. Many strategies exist for achieveing this end. The following outines one path to succes.

### Dump the database

Go to remote location (e.g., a server, your friend's computer), and run:

```
pg_dump -Fc -U postgres opencivicdata > /tmp/ocd.dump
```

`-Fc` tells postgres to use a custom format archive file, which compresses the dump into a relatively smaller file size. You can also employ the `-Z` argument to specify compression size.

### Move the database and restore it

On your local machine, retrieve the database from its remote location, for example:

```
scp ubuntu@ocd.datamade.us:/tmp/ocd.dump ~/Desktop
```

Then, restore it:

```
pg_restore -C -j4 --no-owner /tmp/ocd.dump | psql
```

The `-C` argument creates the database, and the `-j4` argument tells psql to parallelize the process (i.e., use multiple threads and speed up the restore). 

[Official psql documentation](https://www.postgresql.org/docs/current/static/app-pgdump.html)

