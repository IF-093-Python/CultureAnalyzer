import sys

from .default import *

try:
    # Flag DOCKER_ENABLE switch in docker-entrypoint.sh file to 'True'
    # after docker-compose up
    if os.getenv('DOCKER_ENABLE') == 'True':
        from .docker import *
    else:
        from .local import *
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
