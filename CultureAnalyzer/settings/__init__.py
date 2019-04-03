import sys

from .default import *

try:
    if 'runserver' in sys.argv:
        from .local import *
    else:
        from .docker import *
except ImportError:
    pass

try:
    from .production import *
except ImportError:
    pass

if 'test' in sys.argv:
    try:
        from .test import *
    except ImportError:
        pass
