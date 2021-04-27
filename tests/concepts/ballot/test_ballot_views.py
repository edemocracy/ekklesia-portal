import factory
from ekklesia_portal.datamodel import  Ballot

from assert_helpers import assert_difference
from webtest_helpers import assert_deform, fill_form


def test_create_ballot(client, db_query, db_session, ballot_factory, voting_phase_factory, proposition_type_factory, logged_in_department_admin):
    data = factory.build(dict, FACTORY_CLASS=ballot_factory)
    department = logged_in_department_admin.managed_departments[0]
    voting_phase = voting_phase_factory(department=department)
    proposition_type = proposition_type_factory()
    area = department.areas[0]
    res = client.get('/b/+new')
    form = assert_deform(res)
    fill_form(form, data, enum_field_names=['voting_type'], skip_field_names=['proposition_type', 'area'])
    form['voting_id'] = voting_phase.id
    form['area_id'] = area.id
    form['proposition_type_id'] = proposition_type.id

    with assert_difference(db_query(Ballot).count, 1):
        form.submit(status=302)


def test_update(db_session, client, ballot_factory, voting_phase_factory, logged_in_department_admin):
    department = logged_in_department_admin.managed_departments[0]
    voting_phase = voting_phase_factory(department=department)
    area = department.areas[0]
    ballot = ballot_factory(area=area)

    res = client.get(f'/b/{ballot.id}/+edit')
    expected = {k: v for k, v in ballot.to_dict().items() if k in ('election', 'id', 'name')}
    form = assert_deform(res, expected)

    form['name'] = 'new name'
    form['voting_id'] = voting_phase.id
    form['area_id'] = area.id
    form.submit(status=302)
    assert ballot.name == 'new name'


def test_update_global_admin(db_session, client, ballot_factory, voting_phase_factory, logged_in_global_admin):
    voting_phase = voting_phase_factory()
    area = voting_phase.department.areas[0]
    ballot = ballot_factory(area=area)

    res = client.get(f'/b/{ballot.id}/+edit')
    expected = {k: v for k, v in ballot.to_dict().items() if k in ('election', 'id', 'name')}
    form = assert_deform(res, expected)

    form['name'] = 'new name'
    form['voting_id'] = voting_phase.id
    form['area_id'] = area.id
    form.submit(status=302)
    assert ballot.name == 'new name'
