from datetime import datetime
import random
import string

from ekklesia_portal.concepts.proposition.proposition_helper import proposition_slug
from ekklesia_portal.enums import PropositionRelationType, PropositionStatus

import factory
from pytest import fixture

from assert_helpers import assert_difference, assert_no_difference
from ekklesia_portal.datamodel import Changeset, Proposition, SecretVoter, Supporter, Tag
from webtest_helpers import assert_deform
from bs4 import BeautifulSoup


def test_index(client):
    """XXX: depends on content from create_test_db.py"""
    res = client.get("/p")
    assert 'Ein Titel' in res


def test_index_sort_by_supporter_count(client):
    """XXX: depends on content from create_test_db.py"""
    res = client.get("/p?sort=supporter")
    assert 'Ein Titel' in res


def test_index_search(client):
    # german search, should find singular "volltextsuche"
    res = client.get('/p?search=volltextsuchen')
    assert 'Volltextsuche' in res
    assert 'Ein Titel' not in res


def test_index_tag(db_query, client):
    """XXX: depends on content from create_test_db.py"""
    tag = db_query(Tag).filter_by(name='Tag1').one()
    res = client.get('/p?tags=Tag1')
    assert tag.name in res
    assert 'Ein Titel' in res


def test_index_without_tags(db_query, client):
    """XXX: depends on content from create_test_db.py"""
    res = client.get('/p?without_tags=Tag1')
    assert 'Ein Titel' not in res
    assert 'Entstehender Antrag' in res


def test_index_status(client):
    """XXX: depends on content from create_test_db.py"""
    res = client.get('/p?status=abandoned')
    assert 'Fallengelassener Antrag' in res
    assert 'Entstehender Antrag' not in res


def test_index_phase(client):
    """XXX: depends on content from create_test_db.py"""
    res = client.get('/p?phase=bpt192')
    assert 'Angenommener Antrag' in res
    assert 'Abgelehnter Antrag' in res
    assert 'Entstehender Antrag' not in res


def test_index_type(client):
    """XXX: depends on content from create_test_db.py"""
    res = client.get('/p?type=PP')
    assert 'Angenommener Antrag' in res
    assert 'Abgelehnter Antrag' in res


def test_index_search_status(client):
    """XXX: depends on content from create_test_db.py"""
    res = client.get('/p?search=PP001&status=scheduled')
    assert 'Ein Titel' in res
    assert 'Antrag mit nicht unterstütztem Ergebnisformat' not in res


def test_index_department_subject_area(client):
    """XXX: depends on content from create_test_db.py"""
    res = client.get('/p?department=Org Schweiz&subject_area=Innerparteiliches')
    assert 'Ein Titel' in res
    assert 'Angenommener Antrag' not in res


def test_index_per_page(client):
    """XXX: depends on content from create_test_db.py"""
    res = client.get('/p?per_page=2')
    assert 'Ein Titel' in res
    assert 'Angenommener Antrag' not in res


def test_index_per_page2(client):
    """XXX: depends on content from create_test_db.py"""
    res = client.get('/p?per_page=2&page=3')
    assert 'Ein Titel' not in res
    assert 'Angenommener Antrag' in res


def test_index_all_prop(client):
    """XXX: depends on content from create_test_db.py"""
    res = client.get('/p?per_page=-1')
    assert 'Ein Titel' in res
    assert 'Angenommener Antrag' in res
    assert 'Abgelehnter Antrag' in res


def test_index_export_csv(client):
    res = client.get('/p?per_page=-1&media_type=text/csv')
    header = "\"Identifier\";\"Submitters\";\"Title\";\"Text\";\"Reason\";\"Category\";\"Tags\";\"Motion block\";\"Origin\""
    assert res.body.decode().startswith(header)
    assert 'Angenommener Antrag' in res
    assert 'Abgelehnter Antrag' in res
    assert 'Täääg3' in res
    assert "\"PP002\";\"egon\";" not in res, "submitters in csv which is not allowed for normal users!"


def test_index_export_csv_as_global_admin(client, logged_in_global_admin):
    res = client.get('/p?per_page=-1&media_type=text/csv')
    assert "\"PP002\";\"egon\";" in res


def assert_proposition_in_html(proposition: Proposition, html: BeautifulSoup, check_for_details: bool = True):
    proposition_el = html.find(id=f"proposition_{proposition.id}")
    proposition_link = proposition_el.find(class_="proposition_title").find("a")
    assert proposition_link.text == proposition.title
    assert str(proposition.id) in proposition_link["href"]

    if check_for_details:
        proposition_details_text = html.find(class_="proposition_details").text
        assert proposition.content in proposition_details_text
        assert "Motivation" in proposition_details_text
        assert proposition.motivation in proposition_details_text

    badges = proposition_el.find(class_="proposition_badges")
    assert badges, "badges not found"
    department_badge = badges.find(class_="department")
    assert department_badge, "department link not found"
    assert department_badge.text == proposition.ballot.area.department.name, "department name doesn't match"
    area_badge = badges.find(class_="area")
    assert area_badge, "area link not found"
    assert area_badge.text == proposition.ballot.area.name, "area name doesn't match"
    tag_badges = badges.find_all(class_="tag")
    assert {t.name for t in proposition.tags} == {b.text for b in tag_badges}, "tag names don't match"


def test_show(client, proposition):
    res = client.get(f"/p/{proposition.id}/{proposition_slug(proposition)}")
    assert_proposition_in_html(proposition, res.html)


def test_show_legacy_id(client, proposition_factory):
    proposition = proposition_factory(id=1, title="test")
    res = client.get("/p/1/test")
    assert_proposition_in_html(proposition, res.html)


def test_show_associated(client, proposition_factory):
    proposition = proposition_factory(title="test proposition")
    counter_proposition = proposition_factory(title="alternative to test", replaces=proposition)
    amendment = proposition_factory(title="amendment for test", modifies=proposition)
    res = client.get(f"/p/{proposition.id}/test-proposition/associated")
    html = res.html

    change_title = html.select_one(".proposition_col.amendments .proposition_small_title a")
    assert change_title.text == amendment.title
    assert str(amendment.id) in change_title["href"]

    counter_title = html.select_one(".proposition_col.counter .proposition_small_title a")
    assert counter_title.text == counter_proposition.title
    assert str(counter_proposition.id) in counter_title["href"]

    assert_proposition_in_html(proposition, html, check_for_details=False)


def test_new_with_data_import(client, logged_in_user):
    from ekklesia_portal.importer import PROPOSITION_IMPORT_HANDLERS

    import_content = 'pre-filled content'
    import_title = 'pre-filled title'

    def import_test(config, from_data):
        if config['base_url'] == 'test' and from_data == '1':
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


def test_create_somewhere_as_global_admin(
    db_query, client, proposition_factory, proposition_type, department, logged_in_global_admin
):
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
    skip_items = [
        'author_id', 'created_at', 'submitted_at', 'qualified_at', 'ballot_id', 'modifies_id', 'replaces_id',
        'search_vector'
    ]
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


@fixture
def supportable_proposition(logged_in_user_with_departments, ballot_factory, proposition_factory):
    user = logged_in_user_with_departments
    area = user.departments[0].areas[0]
    ballot = ballot_factory(area=area)
    proposition = proposition_factory(
        title="test", ballot=ballot, status=PropositionStatus.SUBMITTED, submitted_at=datetime.now()
    )
    return proposition


@fixture
def assert_support(client, db_session, supportable_proposition, logged_in_user_with_departments):
    user = logged_in_user_with_departments
    proposition = supportable_proposition
    support_url = f'/p/{proposition.id}/test/support'

    def _assert_support(data, support_status, http_status=200, htmx=False):

        if data is None:
            res = None
        else:
            headers = {"HX-Request": "true"} if htmx else {}
            res = client.post(support_url, data, headers=headers, status=http_status)

        qq = db_session.query(Supporter).filter_by(member_id=user.id, proposition_id=proposition.id)
        if support_status is None:
            assert qq.scalar() is None, 'supporter present but should not be present'
        else:
            assert qq.filter_by(status=support_status
                                ).scalar() is not None, f'no supporter found with status {support_status}'

        return res

    return _assert_support


def test_support(assert_support):

    # Nothing happened yet.
    assert_support(data=None, support_status=None)

    # Nothing -> active
    assert_support(dict(support="support"), "active", http_status=302)

    # active -> retracted
    assert_support(dict(support="retract"), "retracted", http_status=302)

    # Sending retract twice is still retracted
    # retracted -> retracted
    assert_support(dict(support="retract"), "retracted", http_status=302)

    # retracted -> active
    assert_support(dict(support="support"), "active", http_status=302)

    # Sending support twice is still active
    # active -> active
    assert_support(dict(support="support"), "active", http_status=302)

    # Invalid requests shouldn't change anything and return bad request.
    assert_support(dict(support="invalid"), "active", http_status=400)

    assert_support(dict(), "active", http_status=400)

    # Retracting still works after client has sent invalid things
    # active -> retracted
    assert_support(dict(support="retract"), "retracted", http_status=302)


def test_support_htmx(assert_support):
    # Nothing happened yet.
    assert_support(data=None, support_status=None)

    # Nothing -> active
    res = assert_support(dict(support="support"), "active", htmx=True)
    assert "<html>" not in res, "only snippet expected for HTMX request, this is a full HTML document"
    assert 'value="retract"' in res, "retract support button missing"

    # active -> retracted
    res = assert_support(dict(support="retract"), "retracted", htmx=True)
    assert 'value="support"' in res, "support button missing"


@fixture
def assert_secret_voting(client, db_session, logged_in_user_with_departments, supportable_proposition):

    user = logged_in_user_with_departments
    proposition = supportable_proposition
    secret_voting_url = f'/p/{proposition.id}/test/secret_voting'

    def _assert_secret_voting(data, secret_voting_status, http_status=200, htmx=False):

        if data is None:
            res = None
        else:
            headers = {"HX-Request": "true"} if htmx else {}
            res = client.post(secret_voting_url, data, headers=headers, status=http_status)

        qq = db_session.query(SecretVoter).filter_by(member_id=user.id, ballot_id=proposition.ballot.id)
        if secret_voting_status is None:
            assert qq.scalar() is None, 'secret voter present but should not be present'
        else:
            assert qq.filter_by(status=secret_voting_status).scalar() is not None, f'no secret voter found with status {status}'

        return res

    return _assert_secret_voting


def test_secret_voting(assert_secret_voting):
    # Nothing happened yet.
    assert_secret_voting(data=None, secret_voting_status=None)

    # Nothing -> request
    assert_secret_voting(dict(secret_voting="request"), 'active', http_status=302)

    # active -> retracted
    assert_secret_voting(dict(secret_voting="retract"), 'retracted', http_status=302)

    # Sending retract twice is still retracted
    # retracted -> retracted
    assert_secret_voting(dict(secret_voting="retract"), 'retracted', http_status=302)

    # retracted -> active
    assert_secret_voting(dict(secret_voting="request"), 'active', http_status=302)

    # Twice requested is still active
    # active -> active
    assert_secret_voting(dict(secret_voting="request"), 'active', http_status=302)

    # Invalid requests shouldn't change anything and return bad request.
    assert_secret_voting(dict(secret_voting="invalid"), 'active', http_status=400)
    assert_secret_voting(dict(), 'active', http_status=400)

    # Retracting still works after client has sent invalid things
    # active -> retracted
    assert_secret_voting(dict(secret_voting="retract"), 'retracted', http_status=302)


def test_secret_voting_htmx(assert_secret_voting):
    # Nothing happened yet.
    assert_secret_voting(data=None, secret_voting_status=None)

    # Nothing -> active
    res = assert_secret_voting(dict(secret_voting="request"), 'active', htmx=True)
    assert "<html>" not in res, "only snippet expected for HTMX request, this is a full HTML document"
    assert 'value="retract"' in res, "retract secret voting request button missing"

    # active -> retracted
    res = assert_secret_voting(dict(secret_voting="retract"), 'retracted', htmx=True)
    assert 'value="request"' in res, "request secret voting button missing"


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
