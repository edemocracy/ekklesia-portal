import factory

from assert_helpers import assert_difference, assert_no_difference
from ekklesia_portal.datamodel import Policy
from webtest_helpers import assert_deform, fill_form


def test_create_policy(client, db_query, policy_factory, logged_in_global_admin):
    data = factory.build(dict, FACTORY_CLASS=policy_factory)
    res = client.get('/policies/+new')
    form = assert_deform(res)
    fill_form(form, data, enum_field_names=['majority', 'voting_system'])

    with assert_difference(db_query(Policy).count, 1):
        form.submit(status=302)


def test_update_policy(db_session, client, policy_factory, logged_in_global_admin):
    policy = policy_factory()
    res = client.get(f'/policies/{policy.id}/+edit')
    expected = policy.to_dict()
    form = assert_deform(res, expected)
    form['name'] = 'new name'
    form.submit(status=302)
    assert policy.name == 'new name'
