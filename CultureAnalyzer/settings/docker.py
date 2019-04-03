ALLOWED_HOSTS = ['*']

STATICFILES_DIRS = []
STATIC_ROOT = "/opt/services/CultureAnalyzer/static"
MEDIA_ROOT = "/opt/services/CultureAnalyzer/media/"
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432
    }
}
