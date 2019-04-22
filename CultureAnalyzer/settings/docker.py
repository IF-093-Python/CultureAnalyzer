import os
from celery.schedules import crontab

ALLOWED_HOSTS = ['*']
DEBUG = False

STATICFILES_DIRS = []
STATIC_ROOT = "/opt/services/CultureAnalyzer/static/"
MEDIA_ROOT = "/opt/services/CultureAnalyzer/media/"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('PG_DB'),
        'USER': os.getenv('PG_USER'),
        'PASSWORD': os.getenv('PG_PASSWORD'),
        'HOST': os.getenv('PG_HOST'),
        'PORT': os.getenv('PG_PORT_IN')
    }
}

REDIS_HOST = os.getenv("RD_HOST")
REDIS_PORT = os.getenv("RD_PORT_IN")

CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}'
CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_BEAT_SCHEDULE = {
    # Executes every Monday at 4:20 a.m.
    'clear_sessions_schedule': {
        'task': 'clear-expired-sessions',
        'schedule': crontab(hour=4, minute=20, day_of_week=1),
    }
}
