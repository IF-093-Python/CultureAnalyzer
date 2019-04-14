#!/usr/bin/env bash

python manage.py collectstatic --noinput
python manage.py migrate --no-input
python manage.py loaddata users/fixtures/fixtures.json

mkdir logs
touch ./logs/gunicorn.log ./logs/gunicorn-access.log
tail -n 0 -f ./logs/gunicorn*.log &

gunicorn --bind :8000 CultureAnalyzer.wsgi:application \
         --reload \
         --log-level=info \
         --log-file=./logs/gunicorn.log \
         --access-logfile=./logs/gunicorn-access.log