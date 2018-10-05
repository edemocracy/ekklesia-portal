from webtest_helpers import assert_deform, fill_form
from assert_helpers import assert_difference, assert_no_difference
from ekklesia_portal.enums import VotingStatus
from ekklesia_portal.database.datamodel import VotingPhase


def test_update(db_session, client, ballot, voting_phase_factory, logged_in_department_admin):
    department = logged_in_department_admin.managed_departments[0]
    voting_phase = voting_phase_factory(department=department)
    area = department.areas[0]

    res = client.get(f'/b/{ballot.id}/+edit')
    expected = {k: v for k, v in ballot.to_dict().items() if k in ('election', 'id', 'name')}
    form = assert_deform(res, expected)

    form['name'] = 'new name'
    form['voting_id'] = voting_phase.id
    form['area_id'] = area.id
    form.submit(status=302)
    assert ballot.name == 'new name'
