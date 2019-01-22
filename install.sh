source venv/bin/activate
pip install requirements.txt
python manage.py migrate
python manage.py loaddata users/fixtures/fixtures.json
python manage.py createsuperuser
python manage.py runserver
