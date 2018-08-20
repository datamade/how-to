# Interacting with a remote database

In the course of developing an application, you may want to make use of data that's stored remotely. For instance, DataMade maintains databases of the information scraped for its [Open Civic Data API](http://docs.opencivicdata.org/en/latest/api/index.html).

You can access that data directly via SSH tunneling, or binding a port on your machine to a port on a remote machine. Doing so allows your application to interact with a remote database as if it were local.

## Getting started

### Authenticate

Some servers don't like strangers. If you're dealing with one, [you'll need SSH access](https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys--2). (Not sure? Try running `ssh ubuntu@<your-server.com>` in your terminal.)

### Create the tunnel

Once you're authorized, open your terminal and build the tunnel.

```bash
ssh -L 9000:localhost:5432 ubuntu@<your-server.com>
```

Let's break this down.

`ssh`, or [Secure Shell](https://en.wikipedia.org/wiki/Secure_Shell), is a command to establish encrypted connections between your computer and a remote machine, a.k.a. a server.

The `-L` flag tells `ssh` you'd like to make a **L**ocal tunnel from the port you specify first, `9000`, to the host and port specified next, `localhost:5432`. (Note that `localhost` in this instance is relative to the server, not your local machine; `localhost` on your side is implicit when you use the `-L` flag, unless you explicitly declare an IP address.)

Finally, `ubuntu@<your-server.com>` tells `ssh` we want to connect to the `ocd.datamade.us` server as the user `ubuntu`.

### Connect to the database

Leaving open your first window, open a new terminal tab or window, and connect to the remote database.

```bash
psql -h localhost -p 9000 -U postgres # connect to postgres on localhost:9000 as the postgres user
```

You are now in the interactive Postgres environment you know and love. Get your bearings using the usual commands: `\l` to view available databases and `\c` to connect to them. Once you connect to a database, you can use `\d` to view available tables and SQL to query as normal.

### Extract information

If you want to extract information for local use (i.e. for transformation), exit the interactive terminal with `\q` and use the `psql` command-line interface to dump the output of a `copy` command to a CSV.

```bash
psql -h localhost -p 9000 -U postgres -d <DATABASE> -c "copy (<QUERY>) to stdout csv header" > shiny_new_data.csv
```

## Supplementary reading

[This is a great blog post](http://blog.trackets.com/2014/05/17/ssh-tunnel-local-and-remote-port-forwarding-explained-with-examples.html) that covers the above, as well as how to forward a port on your machine to a server where your friends can access it, which is sort of like a hacker high-five if you think about it. 🤔