from munch import Munch
from arguments.app import make_wsgi_app
app = make_wsgi_app("config.yml")
from arguments import database
from arguments.app import App
from arguments.database.datamodel import *

s = database.Session()
q = s.query

ip = get_ipython()

ip.magic("autocall 2")
