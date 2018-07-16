from ekklesia_portal.database.datamodel import Supporter
from webtest_helpers import assert_deform

def test_index(client):
    """XXX: depends on content from create_test_db.py"""
    res = client.get("/propositions")
    content = res.body.decode()
    assert content.startswith("<!DOCTYPE html5>")
    assert 'Q1' in content


def test_show(client):
    """XXX: depends on content from create_test_db.py"""
    res = client.get("/propositions/1")
    content = res.body.decode()
    assert content.startswith("<!DOCTYPE html5>")
    assert 'Ein Titel' in content


def test_new_with_data_import(client, logged_in_user):
    from ekklesia_portal.importer import PROPOSITION_IMPORT_HANDLERS

    import_content = 'pre-filled content'
    import_title = 'pre-filled title'

    def import_test(base_url, from_data):
        if base_url == 'test' and from_data == '1':
            return dict(title=import_title, content=import_content)

    PROPOSITION_IMPORT_HANDLERS['test_source'] = import_test

    res = client.get('/propositions/+new?source=test&from_data=1')
    form = res.forms['deform']

    expected = {
        'title': 'pre-filled title',
        'content': 'pre-filled content'
    }
    assert_deform(res, expected)


def test_support(client, db_session, logged_in_user):

    def assert_supporter(status):
        qq = db_session.query(Supporter).filter_by(member_id=logged_in_user.id, proposition_id=3)
        if status is None:
            assert qq.scalar() is None, 'supporter present but should not be present'
        else:
            assert qq.filter_by(status=status).scalar() is not None, f'no supporter found with status {status}'

    res = client.post('/propositions/3/support', dict(support=True), status=302)
    assert_supporter('active')

    res = client.post('/propositions/3/support', dict(retract=True), status=302)
    assert_supporter('retracted')

    res = client.post('/propositions/3/support', dict(retract=True), status=302)
    assert_supporter('retracted')

    res = client.post('/propositions/3/support', dict(support=True), status=302)
    assert_supporter('active')

    res = client.post('/propositions/3/support', dict(support=True), status=302)
    assert_supporter('active')

    res = client.post('/propositions/3/support', dict(invalid=True), status=400)
    assert_supporter('active')

    res = client.post('/propositions/3/support', dict(retract=True), status=302)
    assert_supporter('retracted')

