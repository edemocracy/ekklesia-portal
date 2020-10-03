import random
import string
from ekklesia_portal.concepts.proposition.proposition_helper import proposition_slug
from ekklesia_portal.enums import PropositionRelationType, PropositionStatus

import factory

from assert_helpers import assert_difference, assert_no_difference
from ekklesia_portal.datamodel import Changeset, Proposition, Supporter, Tag
from webtest_helpers import assert_deform


def test_index(client):
    """XXX: depends on content from create_test_db.py"""
    res = client.get("/p")
    content = res.body.decode()
    assert content.startswith("<!DOCTYPE html5>")
    assert 'Ein Titel' in content


def test_index_sort_by_supporter_count(client):
    """XXX: depends on content from create_test_db.py"""
    res = client.get("/p?sort=supporter")
    content = res.body.decode()
    assert 'Ein Titel' in content


def test_index_search(client):
    # german search, should find singular "volltextsuche"
    res = client.get('/p?search=volltextsuchen')
    content = res.body.decode()
    assert content.startswith("<!DOCTYPE html5>")
    assert 'Volltextsuche' in content
    assert 'Ein Titel' not in content


def test_index_tag(db_query, client):
    """XXX: depends on content from create_test_db.py"""
    tag = db_query(Tag).filter_by(name='Tag1').one()
    res = client.get('/p?tags=Tag1')
    content = res.body.decode()
    assert tag.name in content
    assert 'Ein Titel' in content


def test_index_status(client):
    """XXX: depends on content from create_test_db.py"""
    res = client.get('/p?status=abandoned')
    content = res.body.decode()
    assert 'Fallengelassener Antrag' in content
    assert 'Entstehender Antrag' not in content


def test_index_phase(client):
    """XXX: depends on content from create_test_db.py"""
    res = client.get('/p?phase=bpt192')
    content = res.body.decode()
    assert 'Angenommener Antrag' in content
    assert 'Abgelehnter Antrag' in content
    assert 'Entstehender Antrag' not in content


def test_index_type(client):
    """XXX: depends on content from create_test_db.py"""
    res = client.get('/p?type=PP')
    content = res.body.decode()
    assert 'Angenommener Antrag' in content
    assert 'Abgelehnter Antrag' in content


def test_index_search_status(client):
    """XXX: depends on content from create_test_db.py"""
    res = client.get('/p?search=PP001&status=scheduled')
    content = res.body.decode()
    assert 'Ein Titel' in content
    assert 'Antrag mit nicht unterstütztem Ergebnisformat' not in content


def test_index_department_subject_area(client):
    """XXX: depends on content from create_test_db.py"""
    res = client.get('/p?department=Piratenpartei Schweiz&subject_area=Innerparteiliches')
    content = res.body.decode()
    assert 'Ein Titel' in content
    assert 'Angenommener Antrag' not in content


def test_show(client, proposition):
    res = client.get(f"/p/{proposition.id}/{proposition_slug(proposition)}")
    content = res.body.decode()
    assert content.startswith("<!DOCTYPE html5>")
    assert proposition.title in content
    assert proposition.content in content


def test_show_legacy_id(client, proposition_factory):
    proposition_factory(id=1, title="test")
    client.get("/p/1/test")


def test_show_associated(client, proposition_factory):
    proposition = proposition_factory(title="test proposition")
    counter_proposition = proposition_factory(title="alternative to test", replaces=proposition)
    change_proposition = proposition_factory(title="change test", modifies=proposition)
    res = client.get(f"/p/{proposition.id}/test-proposition/associated")
    content = res.body.decode()
    assert content.startswith("<!DOCTYPE html5>")
    assert counter_proposition.title in content
    assert change_proposition.title in content
    assert proposition.title in content


def test_new_with_data_import(client, logged_in_user):
    from ekklesia_portal.importer import PROPOSITION_IMPORT_HANDLERS

    import_content = 'pre-filled content'
    import_title = 'pre-filled title'

    def import_test(base_url, from_data):
        if base_url == 'test' and from_data == '1':
            return dict(title=import_title, content=import_content)

    PROPOSITION_IMPORT_HANDLERS['test_source'] = import_test

    res = client.get('/p/+new?source=test&from_data=1')
    expected = {'title': 'pre-filled title', 'content': 'pre-filled content'}
    assert_deform(res, expected)


def test_create(db_query, client, proposition_factory, proposition_type, logged_in_user_with_departments):
    user = logged_in_user_with_departments
    data = factory.build(dict, FACTORY_CLASS=proposition_factory)
    related_proposition_id = proposition_factory().id
    data['tags'] = 'Tag1,' + "".join(random.choices(string.ascii_lowercase, k=10)).capitalize()
    data['status'] = data['status'].name
    data['area_id'] = user.departments[0].areas[0].id
    data['proposition_type_id'] = proposition_type.id
    data['related_proposition_id'] = related_proposition_id
    data['relation_type'] = PropositionRelationType.MODIFIES.name
    data['external_discussion_url'] = 'http://example.com'

    with assert_difference(db_query(Proposition).count, 1, 'proposition'):
        with assert_difference(db_query(Tag).count, 1, 'tag'):
            client.post('/p', data, status=302)

    proposition = db_query(Proposition).order_by(Proposition.id.desc()).limit(1).first()
    related_proposition = db_query(Proposition).get(related_proposition_id)
    assert proposition.modifies == related_proposition

    data['relation_type'] = PropositionRelationType.REPLACES.name
    client.post('/p', data, status=302)

    proposition = db_query(Proposition).order_by(Proposition.id.desc()).limit(1).first()
    assert proposition.replaces == related_proposition


def test_create_somewhere_as_global_admin(db_query, client, proposition_factory, proposition_type, department, logged_in_global_admin):
    """Global admin user should be able to create a proposition regardless of department membership"""
    data = factory.build(dict, FACTORY_CLASS=proposition_factory)
    data['area_id'] = department.areas[0].id
    data['proposition_type_id'] = proposition_type.id

    # Check precondition: admin is not member of the department
    assert department not in logged_in_global_admin.departments

    # Proposition should be created
    with assert_difference(db_query(Proposition).count, 1, 'proposition'):
        client.post('/p', data, status=302)


def test_update_as_global_admin(client, proposition_factory, logged_in_global_admin):

    proposition = proposition_factory(title="test")

    res = client.get(f'/p/{proposition.id}/test/edit')
    skip_items = ['created_at', 'submitted_at', 'qualified_at', 'ballot_id', 'modifies_id', 'replaces_id', 'search_vector']
    expected = {k: v for k, v in proposition.to_dict().items() if k not in skip_items}
    form = assert_deform(res, expected)

    form['title'] = 'new title'
    form['status'] = 'ABANDONED'
    form.submit(status=302)
    assert proposition.title == 'new title'
    assert proposition.status == PropositionStatus.ABANDONED


def test_does_not_create_without_title(db_query, client, proposition_factory, logged_in_user):
    data = factory.build(dict, FACTORY_CLASS=proposition_factory)
    data['proposition_type_id'] = 1
    data['area_id'] = 1
    del data['title']

    with assert_no_difference(db_query(Proposition).count):
        client.post('/p', data, status=200)


def test_support(client, db_session, logged_in_user, proposition_factory):

    proposition = proposition_factory(title="test")

    def assert_supporter(status):
        qq = db_session.query(Supporter).filter_by(member_id=logged_in_user.id, proposition_id=proposition.id)
        if status is None:
            assert qq.scalar() is None, 'supporter present but should not be present'
        else:
            assert qq.filter_by(status=status).scalar() is not None, f'no supporter found with status {status}'

    support_url = f'/p/{proposition.id}/test/support'

    client.post(support_url, dict(support=True), status=302)
    assert_supporter('active')

    client.post(support_url, dict(retract=True), status=302)
    assert_supporter('retracted')

    client.post(support_url, dict(retract=True), status=302)
    assert_supporter('retracted')

    client.post(support_url, dict(support=True), status=302)
    assert_supporter('active')

    client.post(support_url, dict(support=True), status=302)
    assert_supporter('active')

    client.post(support_url, dict(invalid=True), status=400)
    assert_supporter('active')

    client.post(support_url, dict(retract=True), status=302)
    assert_supporter('retracted')


def test_redirect_to_full_url(client, proposition_factory):
    proposition = proposition_factory(title="test")
    res = client.get(f'/p/{proposition.id}', status=302)
    assert res.headers['Location'] == f'http://localhost/p/{proposition.id}/test'


def test_new_draft(db_query, client, proposition_factory, document, logged_in_user):
    logged_in_user.departments.append(document.area.department)
    data = factory.build(dict, FACTORY_CLASS=proposition_factory)
    data['tags'] = 'Tag1,' + "".join(random.choices(string.ascii_lowercase, k=10)).capitalize()
    data['editing_remarks'] = 'editing remarks'

    with assert_no_difference(db_query(Proposition).count, 'proposition'):
        with assert_no_difference(db_query(Tag).count, 'tag'):
            resp = client.post(f'/p/+new_draft?document={document.id}', data, status=200)

    data['document_id'] = document.id
    data['section'] = '1.1'

    with assert_difference(db_query(Proposition).count, 1, 'proposition'):
        with assert_difference(db_query(Tag).count, 1, 'tag'):
            with assert_difference(db_query(Changeset).count, 1, 'changeset'):
                client.post('/p/+new_draft', data, status=302)
