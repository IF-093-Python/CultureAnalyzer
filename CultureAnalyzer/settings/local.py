import CultureAnalyzer
from .base_settings import *

DEBUG = True
ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cultureAnalyzer',
        'USER': 'postgres',
        'PASSWORD': '1516',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
