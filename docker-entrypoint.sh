#!/usr/bin/env bash

mkdir logs
touch ./logs/gunicorn.log
touch ./logs/gunicorn-access.log
tail -n 0 -f ./logs/gunicorn*.log &

export DOCKER_FLAG=true

python manage.py collectstatic --noinput
python manage.py migrate --no-input
python manage.py loaddata users/fixtures/fixtures.json

gunicorn --bind :8000 CultureAnalyzer.wsgi:application \
--log-level=info \
--log-file=./logs/gunicorn.log \
--access-logfile=./logs/gunicorn-access.log

exec "$@"
