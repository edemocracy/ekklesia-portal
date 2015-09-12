from arguments import make_app
app = make_app()
from arguments import db
from arguments.database.datamodel import *
s = db.session
q = s.query

ip = get_ipython()

ip.magic("autocall 2")
