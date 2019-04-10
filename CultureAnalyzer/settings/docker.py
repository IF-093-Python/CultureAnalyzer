import os

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
