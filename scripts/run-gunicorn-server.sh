#!/usr/bin/env bash

python manage.py collectstatic --noinput
python manage.py migrate --no-input
python manage.py loaddata users/fixtures/fixtures.json

mkdir logs
touch ./logs/gunicorn.log ./logs/gunicorn-access.log ./logs/celery.log
tail -n 0 -f ./logs/*.log &

celery worker \
        --beat \
        --app=CultureAnalyzer \
        --schedule=/tmp/celerybeat-schedule \
        --pidfile=/tmp/celeryd.pid  \
        --logfile=./logs/celery.log \
        --loglevel=info &

gunicorn --bind :8000 CultureAnalyzer.wsgi:application \
         --reload \
         --log-level=info \
         --log-file=./logs/gunicorn.log \
         --access-logfile=./logs/gunicorn-access.log

exec "$@"