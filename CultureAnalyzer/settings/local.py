import CultureAnalyzer
from .base_settings import *

DEBUG = True
ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cultureanalyzer',
        'USER': 'analyzer',
        'PASSWORD': 'qwerty12345',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}