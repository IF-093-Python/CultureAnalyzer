from .base_settings import *

ALLOWED_HOSTS = ['*']

DEBUG = False

STATIC_URL = '/static/'

# as declared in NginX conf, it must match /opt/services/djangoapp/static/
STATIC_ROOT = "/var/www/CultureAnalyzer/static/"

# do the same for media files, it must match /opt/services/djangoapp/media/
MEDIA_ROOT = "/var/www/CultureAnalyzer/media/"
