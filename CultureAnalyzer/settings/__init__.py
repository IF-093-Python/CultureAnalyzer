import sys

from .default import *

try:
    docker_enable = os.getenv('DOCKER_ENABLE', 'False') == 'True'
    if docker_enable:
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
