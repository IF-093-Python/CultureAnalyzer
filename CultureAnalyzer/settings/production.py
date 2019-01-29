from .base_settings import *


DEBUG = False
ALLOWED_HOSTS = ['*']

STATIC_URL = '/static/'

# as declared in NginX conf, it must match /opt/services/djangoapp/static/
STATIC_ROOT = "/var/www/CultureAnalyzer/static/"

# do the same for media files, it must match /opt/services/djangoapp/media/
MEDIA_ROOT = "/var/www/CultureAnalyzer/media/"
