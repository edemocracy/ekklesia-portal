import factory

from assert_helpers import assert_difference, assert_no_difference
from ekklesia_portal.datamodel import Document
from webtest_helpers import assert_deform, fill_form


def test_create_document(client, db_query, document_factory, proposition_type_factory, logged_in_department_admin):
    department = logged_in_department_admin.managed_departments[0]
    area = department.areas[0]
    proposition_type = proposition_type_factory()
    data = factory.build(dict, FACTORY_CLASS=document_factory)
    del data['area']
    data['area_id'] = area.id
    del data['proposition_type']
    data['proposition_type_id'] = proposition_type.id
    res = client.get('/documents/+new')
    form = assert_deform(res)
    fill_form(form, data)

    with assert_difference(db_query(Document).count, 1):
        form.submit(status=302)


def test_update_document(db_session, client, document_factory, logged_in_department_admin):
    department = logged_in_department_admin.managed_departments[0]
    area = department.areas[0]
    document = document_factory(area=area)
    res = client.get(f'/documents/{document.id}/+edit')
    expected = document.to_dict()
    form = assert_deform(res, expected)
    form['description'] = 'new description'
    form.submit(status=302)
    assert document.description == 'new description'
