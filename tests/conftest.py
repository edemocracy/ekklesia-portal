import logging
import os.path
import sys

from .factories import *
from .fixtures import *

sys.path.append(os.path.join(os.path.dirname(__file__), 'helpers'))

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('morepath').setLevel(logging.INFO)

logg = logging.getLogger('test')
