import datetime

import factory

from assert_helpers import assert_difference
from ekklesia_portal.datamodel import VotingPhase
from ekklesia_portal.enums import VotingStatus
from webtest_helpers import assert_deform, fill_form


def test_create_voting_phase(client, db_query, voting_phase_type, voting_phase_factory, logged_in_department_admin):
    data = factory.build(dict, FACTORY_CLASS=voting_phase_factory)
    department = logged_in_department_admin.managed_departments[0]

    res = client.get('/v/+new')
    form = assert_deform(res)
    department_options = form.fields['department_id'][0].options
    assert len(department_options) == 1, 'should have exactly one department option'
    assert department_options[0][2] == department.name

    fill_form(form, data, ['title', 'name', 'secret', 'description'])
    form.set('date', data['target'], index=0)
    form['department_id'] = department.id
    form['phase_type_id'] = voting_phase_type.id
    form['status'] = VotingStatus.PREPARING.name

    with assert_difference(db_query(VotingPhase).count, 1):
        form.submit(status=302)


def test_update_voting_phase(client, voting_phase_factory, logged_in_department_admin):
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


def test_create_as_global_admin(db_query, client, voting_phase_factory, voting_phase_type, logged_in_global_admin):
    """Global admin user should be able to update a voting phase regardless of department membership"""

    data = factory.build(dict, FACTORY_CLASS=voting_phase_factory)

    res = client.get('/v/+new')
    form = assert_deform(res)

    fill_form(form, data, ['title', 'name', 'secret', 'description'])
    form.set('date', data['target'], index=0)
    form['phase_type_id'] = voting_phase_type.id

    with assert_difference(db_query(VotingPhase).count, 1):
        form.submit(status=302)

def test_update_as_global_admin(client, voting_phase_factory, logged_in_global_admin):
    voting_phase = voting_phase_factory()
    res = client.get(f'/v/{voting_phase.id}/slug/+edit')
    expected = voting_phase.to_dict()
    expected['date'] = expected['target']
    del expected['target']
    form = assert_deform(res, expected)

    form['title'] = 'new title'
    form.submit(status=302)
    assert voting_phase.title == 'new title'


def test_create_voting(client, department_factory, voting_phase_factory, logged_in_global_admin, monkeypatch):

    department = department_factory(voting_module_settings={"test": {}})
    voting_phase: VotingPhase = voting_phase_factory(
        department=department,
        target=datetime.datetime.now(),
        registration_start_days=21,
        voting_days=14
    )

    def _create_test_voting(_module_config, _voting_phase):
        assert _module_config["api_urls"]
        assert _voting_phase is voting_phase
        return {"result_url": "http://test1/result"}

    def _retrieve_test_voting(_module_config, _voting_data):
        return {}

    monkeypatch.setattr("ekklesia_portal.voting_modules.VOTING_MODULES", {"test": (_create_test_voting, _retrieve_test_voting)})

    res = client.post(f"/v/{voting_phase.id}/slug/create_voting", dict(create_voting="test"), status=302)
    loc = res.headers["Location"]
    assert str(voting_phase.id) in loc, res.headers

    assert voting_phase.voting_module_data.get("test", {}).get("result_url") == "http://test1/result", voting_phase.voting_module_data
