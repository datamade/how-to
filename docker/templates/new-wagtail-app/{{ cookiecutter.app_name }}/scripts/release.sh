#!/bin/bash
# scripts/release.sh -- Commands to run on every Heroku release

set -euo pipefail

python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py createcachetable && python manage.py clear_cache

# Check if initial data exists, and if not, import initial pages, etc.
if [ `psql ${DATABASE_URL} -tAX -c "SELECT COUNT(*) FROM {{ cookiecutter.module_name }}_homepage"` -eq "0" ]; then
   python manage.py load_cms_content
fi
