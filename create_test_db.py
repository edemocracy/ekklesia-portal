import logging
logging.basicConfig(level=logging.INFO)
from munch import Munch
import transaction
from arguments.app import make_wsgi_app

app = make_wsgi_app(Munch(config_file="config.yml"))

logg = logging.getLogger(__name__)


from arguments.database import db_metadata, Session
from arguments.database.datamodel import *


logg.info("using db url %s", app.settings.database.uri)

db_metadata.drop_all()
db_metadata.create_all()

s = Session()

ug1 = Group(name="Deppengruppe")

u1 = User(name="testuser", usertype="system")
u2 = User(name="egon", usertype="system")
ug1.members.extend([u1, u2])

t1 = Tag(name="Tag1")
t2 = Tag(name="Tag2")
t3 = Tag(name="Täääg3")

q1 = Proposition(title="Ein Titel", content="blah")

q1_counter = Proposition(title="Gegenantrag zu Q1", content="will was anderes", replaces=q1)
s.add(q1_counter)

q1_counter_2 = Proposition(title="Noch ein Gegenantrag zu Q1", content="will was ganz anderes", replaces=q1)
s.add(q1_counter_2)

q1_change = Proposition(title="Änderungsantrag zu Q1", content="will was ändern", modifies=q1)
s.add(q1_change)

arg1 = Argument(author=u1, title="Ein Pro-Argument", abstract="dafür abstract", details="dafür")
arg2 = Argument(author=u2, title="Ein zweites Pro-Argument", abstract="dafür!!!")
arg3 = Argument(author=u1, title="Ein Contra-Argument", abstract="dagegen abstract", details="dafür")

arg1_rel = ArgumentRelation(proposition=q1, argument=arg1, argument_type="pro")
arg2_rel = ArgumentRelation(proposition=q1, argument=arg2, argument_type="con")
arg3_rel = ArgumentRelation(proposition=q1, argument=arg3, argument_type="pro")

q1.proposition_arguments.extend([arg1_rel, arg2_rel, arg3_rel])
q1.tags.extend([t1, t2])
s.add(q1)

q2 = Proposition(title="Noch Ein Titel", content="blah")
q2.tags.append(t3)
s.add(q2)

qv1 = Supporter(member=u1, proposition=q1, submitter=True)
s.add(qv1)
qv2 = Supporter(member=u2, proposition=q1_counter, submitter=True)
s.add(qv2)
qv3 = Supporter(member=u1, proposition=q2)
s.add(qv3)

qv1 = ArgumentVote(member=u1, relation=arg1_rel, weight=1)
s.add(qv1)
qv2 = ArgumentVote(member=u1, relation=arg2_rel, weight=-1)
s.add(qv2)
qv3 = ArgumentVote(member=u2, relation=arg1_rel, weight=-1)
s.add(qv3)

transaction.commit()

logg.info("commited")