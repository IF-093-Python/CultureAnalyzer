#!/usr/bin/env bash
pip install -r config/requirements/app.pip
python manage.py migrate
python manage.py loaddata users/fixtures/fixtures.json
python manage.py createsuperuser
