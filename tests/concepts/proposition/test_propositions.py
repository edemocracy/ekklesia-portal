import random
import string
from ekklesia_portal.database.datamodel import Supporter, Proposition, Tag
from webtest_helpers import assert_deform
from assert_helpers import assert_difference, assert_no_difference


def test_index(client):
    """XXX: depends on content from create_test_db.py"""
    res = client.get("/propositions")
    content = res.body.decode()
    assert content.startswith("<!DOCTYPE html5>")
    assert 'Q1' in content


def test_index_mode_top(client):
    """XXX: depends on content from create_test_db.py"""
    res = client.get("/propositions?mode=top")
    content = res.body.decode()
    assert 'Q1' in content


def test_index_search(client):
    # german search, should find singular "volltextsuche"
    res = client.get('/propositions?search=volltextsuchen')
    content = res.body.decode()
    assert content.startswith("<!DOCTYPE html5>")
    assert 'Volltextsuche' in content
    assert 'Titel' not in content


def test_index_tag(db_query, client):
    tag = db_query(Tag).filter_by(name='Tag1').one()
    res = client.get('/propositions?tag=Tag1')
    content = res.body.decode()
    assert tag.name in content
    assert 'Ein Titel' in content


def test_show(client):
    """XXX: depends on content from create_test_db.py"""
    res = client.get("/propositions/1")
    content = res.body.decode()
    assert content.startswith("<!DOCTYPE html5>")
    assert 'Ein Titel' in content


def test_show_associated(client):
    """XXX: depends on content from create_test_db.py"""
    res = client.get("/propositions/1/associated")
    content = res.body.decode()
    assert content.startswith("<!DOCTYPE html5>")
    assert 'Ein Titel' in content
    assert 'Gegenantrag' in content
    assert 'Änderungsantrag' in content


def test_new_with_data_import(client, logged_in_user):
    from ekklesia_portal.importer import PROPOSITION_IMPORT_HANDLERS

    import_content = 'pre-filled content'
    import_title = 'pre-filled title'

    def import_test(base_url, from_data):
        if base_url == 'test' and from_data == '1':
            return dict(title=import_title, content=import_content)

    PROPOSITION_IMPORT_HANDLERS['test_source'] = import_test

    res = client.get('/propositions/+new?source=test&from_data=1')
    expected = {
        'title': 'pre-filled title',
        'content': 'pre-filled content'
    }
    assert_deform(res, expected)


def test_create(db_query, client, proposition_factory, logged_in_user_with_departments):
    user = logged_in_user_with_departments
    # XXX: this is stubid... Is there a better way to get a simple dict from factory boy? Do we need a new strategy?
    data = dict(proposition_factory.stub().__dict__)
    data['tags'] = 'Tag1,' + "".join(random.choices(string.ascii_lowercase, k=10)).capitalize()

    data['area_id'] = user.departments[0].areas[0].id
    data['related_proposition_id'] = 3
    data['relation_type'] = 'modifies'

    with assert_difference(db_query(Proposition).count, 1, 'proposition'):
        with assert_difference(db_query(Tag).count, 1, 'tag'):
            client.post('/propositions', data, status=302)

    proposition = db_query(Proposition).order_by(Proposition.id.desc()).limit(1).first()
    other_proposition = db_query(Proposition).get(3)
    assert proposition.modifies == other_proposition

    data['relation_type'] = 'replaces'
    client.post('/propositions', data, status=302)

    proposition = db_query(Proposition).order_by(Proposition.id.desc()).limit(1).first()
    assert proposition.replaces == other_proposition


def test_does_not_create_without_title(db_query, client, proposition_factory, logged_in_user):
    # XXX: this is stubid... Is there a better way to get a simple dict from factory boy? Do we need a new strategy?
    data = dict(proposition_factory.stub().__dict__)
    del data['title']

    with assert_no_difference(db_query(Proposition).count):
        client.post('/propositions', data, status=200)


def test_support(client, db_session, logged_in_user):
    def assert_supporter(status):
        qq = db_session.query(Supporter).filter_by(member_id=logged_in_user.id, proposition_id=3)
        if status is None:
            assert qq.scalar() is None, 'supporter present but should not be present'
        else:
            assert qq.filter_by(status=status).scalar() is not None, f'no supporter found with status {status}'

    client.post('/propositions/3/support', dict(support=True), status=302)
    assert_supporter('active')

    client.post('/propositions/3/support', dict(retract=True), status=302)
    assert_supporter('retracted')

    client.post('/propositions/3/support', dict(retract=True), status=302)
    assert_supporter('retracted')

    client.post('/propositions/3/support', dict(support=True), status=302)
    assert_supporter('active')

    client.post('/propositions/3/support', dict(support=True), status=302)
    assert_supporter('active')

    client.post('/propositions/3/support', dict(invalid=True), status=400)
    assert_supporter('active')

    client.post('/propositions/3/support', dict(retract=True), status=302)
    assert_supporter('retracted')
