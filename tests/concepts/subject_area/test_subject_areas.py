import factory
from webtest_helpers import assert_deform, fill_form
from assert_helpers import assert_difference, assert_no_difference
from ekklesia_portal.datamodel import SubjectArea


def test_create_subject_area(client, db_query, subject_area_factory, logged_in_department_admin):
    department = logged_in_department_admin.managed_departments[0]
    data = factory.build(dict, FACTORY_CLASS=subject_area_factory)
    del data["department"]
    data["department_id"] = department.id

    res = client.get('/subject_areas/+new')
    form = assert_deform(res)
    fill_form(form, data, ['name'])

    with assert_difference(db_query(SubjectArea).count, 1):
        form.submit(status=302)


def test_update_subject_area(db_session, client, subject_area_factory, logged_in_department_admin):
    department = logged_in_department_admin.managed_departments[0]
    subject_area = subject_area_factory(department=department)
    res = client.get(f'/subject_areas/{subject_area.id}/+edit')
    expected = subject_area.to_dict()
    form = assert_deform(res, expected)
    form['name'] = 'new name'
    form.submit(status=302)
    assert subject_area.name == 'new name'
