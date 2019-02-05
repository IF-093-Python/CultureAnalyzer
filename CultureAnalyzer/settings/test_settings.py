import sys
from .base_settings import *

if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'culture_analyzer_test'
        }
    }
