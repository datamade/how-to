#!/bin/sh
set -e

if [ "$DJANGO_MANAGEPY_MIGRATE" = 'on' ]; then
    python manage.py migrate --noinput
fi

exec "$@"
