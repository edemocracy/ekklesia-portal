# coding: utf8
from arguments import make_app
app = make_app()
from arguments import db
from arguments.database.new_datamodel import *

db.drop_all()
db.create_all()

s = db.session

ug1 = Group(name="Deppengruppe")

u1 = User(name="testuser")

u2 = User(name="egon")

ug1.users.extend([u1, u2])

t1 = Tag(name="Tag1")
t2 = Tag(name="Tag2")
t3 = Tag(name="Täääg3")

q1 = Proposition(title="Ein Titel", content="blah")

q1_counter = Proposition(url="Q1Counter", title="Gegenantrag zu Q1", details="will was anderes", replaces=q1)
s.add(q1_counter)

q1_counter_2 = Proposition(url="Q1Counter2", title="Noch ein Gegenantrag zu Q1", details="will was ganz anderes", replaces=q1)
s.add(q1_counter_2)

q1_change = Proposition(url="Q1Change", title="Änderungsantrag zu Q1", details="will was ändern", modifies=q1)
s.add(q1_change)

arg1 = Argument(proposition=q1, author=u1, title="Ein Pro-Argument",
                abstract="dafür abstract", details="dafür", argument_type="pro")

ca1_1 = Argument(proposition=q1, author=u2, title="Gegenargument", 
                 argument_type="con", abstract="Abstract ca_1_1", details="mäh", parent=arg1)

arg2 = Argument(proposition=q1, author=u2, title="Ein zweites Pro-Argument",
                abstract="dafür!!!", argument_type="pro")

arg3 = Argument(proposition=q1, author=u1, title="Ein Contra-Argument",
                abstract="dagegen abstract", details="dafür", argument_type="con")

q1.arguments.extend([arg1, arg2, arg3, ca1_1])
q1.tags.extend([t1, t2])
s.add(q1)

q2 = Proposition(url="A2", title="Noch Ein Titel", details="blah")
q2.tags.append(t3)
s.add(q2)

qv1 = PropositionVote(user=u1, proposition=q1)
s.add(qv1)
qv2 = PropositionVote(user=u1, proposition=q2)
s.add(qv2)
qv3 = PropositionVote(user=u2, proposition=q1)
s.add(qv3)

qv1 = ArgumentVote(user=u1, argument=arg1, value=1)
s.add(qv1)
qv2 = ArgumentVote(user=u1, argument=arg2, value=-1)
s.add(qv2)
qv3 = ArgumentVote(user=u2, argument=arg1, value=1)
s.add(qv3)

s.commit()
