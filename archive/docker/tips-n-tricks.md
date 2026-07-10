# Useful commands
Here's a collection of useful commands for using docker within DataMade's stack.

## Reclaiming space
Sometimes docker behaves weirdly and fails to build / restarts suddenly. This is typically because it ran out of hard drive space.

### Delete the orphaned volumes in Docker

```bash
docker volume rm $(docker volume ls -qf dangling=true)
```

List dangling volumes:

```bash
docker volume ls -qf dangling=true
```

List all volumes:

```bash
docker volume ls
```

### Delete unused images
Remove `<none>` images that sometimes get generated when a Docker build is interrupted and then hang around:

```bash
docker rmi $(docker images | grep '^<none>' | awk '{print $3}')
```

## Miscellaneous
Connect to the container's bash session:
```bash
docker-compose run --rm app bash
```

Connect to the Django shell:
```bash
docker-compose run --rm app python manage.py shell
```

List all of the running containers:
```bash
docker ps
```

Kill a specific container:
```bash
docker kill <pid> # you got the PID from the docker ps command
```

Remove all volumes from your machine (this one will take a while and will require you to rebuild any image you want to use again):
```bash
docker system prune --all
```


Build without using the cache:
```bash
docker-compose build --no-cache
```

Add a new npm package:
```bash
docker-compose run --rm app npm install <package-name>
```


List all the containers (not only the running ones):
```bash
docker ps -a
```

Debug your image:
```bash
docker logs <my-container-image>
```

Attach to a pdb session. First get the process id (via `docker ps`) and then:
```bash
docker attach 833ec224bdeb
```
