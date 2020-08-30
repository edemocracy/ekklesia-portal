import factory

from ekklesia_portal.datamodel import Proposition


def test_proposition(db_session, proposition_factory):
    data = factory.build(dict, FACTORY_CLASS=proposition_factory)
    proposition = Proposition(**data)
    db_session.add(proposition)
    db_session.flush()

