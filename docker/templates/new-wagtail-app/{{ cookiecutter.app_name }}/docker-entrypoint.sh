#!/bin/sh
set -e

# https://github.com/docker-library/postgres/issues/146#issuecomment-872486465
# If postgres isn't ready yet, wait and try again 
readonly SLEEP_TIME=5
readonly PG_HOST="{{ cookiecutter.module_name}}-postgres"
readonly PG_USER="postgres"
readonly PG_DB="{{ cookiecutter.module_name }}"

# note: the PGPASSWORD envar is passed in
until timeout 3 psql -h $PG_HOST -U $PG_USER -c "select 1" -d $PG_DB > /dev/null
do
  printf "Waiting %s seconds for PostgreSQL to come up: %s@%s/%s...\n" $SLEEP_TIME $PG_USER $PG_HOST $PG_DB
  sleep $SLEEP_TIME;
done

if [ "$DJANGO_MANAGEPY_MIGRATE" = 'on' ]; then
    python manage.py migrate --noinput
fi

exec "$@"
