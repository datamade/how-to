#!/bin/bash
# scripts/release.sh -- Commands to run on every Heroku release

set -euo pipefail

python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py createcachetable && python manage.py clear_cache

# Optional: Check if initial data exists, and if not, run initial imports.
# To enable, uncomment this block and change example_data to match a table
# name in your app.
# if [ `psql ${DATABASE_URL} -tAX -c "SELECT COUNT(*) FROM example_table"` -eq "0" ]; then
#    # Define an initial data loading command here, if one exists.
# fi
