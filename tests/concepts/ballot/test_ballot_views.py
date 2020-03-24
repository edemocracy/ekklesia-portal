from webtest_helpers import assert_deform


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
