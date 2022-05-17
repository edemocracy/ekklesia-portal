import factory

from assert_helpers import assert_difference, assert_no_difference
from ekklesia_portal.datamodel import Department
from webtest_helpers import assert_deform, fill_form


def test_create_department(client, db_query, department_factory, logged_in_global_admin):
    data = factory.build(dict, FACTORY_CLASS=department_factory)
    res = client.get('/d/+new')
    form = assert_deform(res)
    fill_form(form, data)

    with assert_difference(db_query(Department).count, 1):
        form.submit(status=302)


def test_update_department(db_session, client, department_factory, logged_in_global_admin):
    department = department_factory()
    res = client.get(f'/d/{ department.id}/+edit')
    expected = department.to_dict()
    form = assert_deform(res, expected)
    form['name'] = 'new name'
    form['description'] = 'new description'
    form.submit(status=302)
    assert department.name == 'new name'
    assert department.description == 'new description'


def test_index(client):
    assert 'Org Deutschland' in client.get('/d')


def test_department_view_not_logged_in(client):
    assert 'My departments' not in client.get('/d')


def test_department_view_logged_in(client, logged_in_user_with_departments):
    res = client.get('/d')
    if logged_in_user_with_departments.departments:
        assert 'My departments' in res
        for department in logged_in_user_with_departments.departments:
            assert department.name in res



