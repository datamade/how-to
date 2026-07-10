# Dockerizing psql

Sometimes, it makes sense to isolate database dependencies when doing local development (e.g., you need to mimic a remote database). Docker saves the day.

### Get postgres 9.6 with postgis

Run the following:

```
docker run --name postgres96 -it -d -v pg96_data:/var/lib/postgresql/data -p 37000:5432 mdillon/postgis:9.6
```

Summation of commands:

`-it` – allows you to run docker from the terminal

`-d` – runs docker as a daemonized process

`-v` – pg96_data: the name of the volume (can be anything)

`-p 37000` – the name of the port (whatever you desire, but should be a large number)

`mdillon/postgis:9.6` – the remote docker file that installs both psql and postgis - https://hub.docker.com/r/mdillon/postgis/~/dockerfile/

### Use docker

Essential commands:

```
# Login to the dockerized version of psql as the postgres user
psql -U postgres -h 127.0.0.1 -p 37000

# Add yourself as psql user
createuser -U postgres -h 127.0.0.1 -p 37000 <your name>

# Create a database with your user name, for easy login
createdb -h 127.0.0.1 -p 37000 <your name>
psql -h 127.0.0.1 -p 37000
```