import factory

from assert_helpers import assert_difference, assert_no_difference
from ekklesia_portal.datamodel import VotingPhase
from ekklesia_portal.enums import VotingStatus
from webtest_helpers import assert_deform, fill_form


def test_create_voting_phase(client, db_query, voting_phase_type, voting_phase_factory, logged_in_department_admin):
    data = factory.build(dict, FACTORY_CLASS=voting_phase_factory)
    department = logged_in_department_admin.managed_departments[0]

    res = client.get('/v/+new')
    form = assert_deform(res)

    fill_form(form, data, ['title', 'name', 'secret', 'description'])
    form.set('date', data['target'], index=0)
    form['department_id'] = department.id
    form['phase_type_id'] = voting_phase_type.id
    form['status'] = VotingStatus.PREPARING.name

    with assert_difference(db_query(VotingPhase).count, 1):
        form.submit(status=302)


def test_update_voting_phase(db_session, client, voting_phase_factory, logged_in_department_admin):
    department = logged_in_department_admin.managed_departments[0]
    voting_phase = voting_phase_factory(department=department)
    res = client.get(f'/v/{voting_phase.id}/slug/+edit')
    expected = voting_phase.to_dict()
    expected['date'] = expected['target']
    del expected['target']
    form = assert_deform(res, expected)

    form['title'] = 'new title'
    form.submit(status=302)
    assert voting_phase.title == 'new title'
