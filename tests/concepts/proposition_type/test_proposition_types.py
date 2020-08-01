import factory

from assert_helpers import assert_difference, assert_no_difference
from ekklesia_portal.datamodel import PropositionType
from webtest_helpers import assert_deform, fill_form


def test_create_proposition_type(client, db_query, proposition_type_factory, logged_in_global_admin):
    data = factory.build(dict, FACTORY_CLASS=proposition_type_factory)
    res = client.get('/proposition_types/+new')
    form = assert_deform(res)
    fill_form(form, data, ['name', 'abbreviation'])

    with assert_difference(db_query(PropositionType).count, 1):
        form.submit(status=302)


def test_update_proposition_type(db_session, client, proposition_type_factory, logged_in_global_admin):
    proposition_type = proposition_type_factory()
    res = client.get(f'/proposition_types/{ proposition_type.id}/+edit')
    expected = proposition_type.to_dict()
    form = assert_deform(res, expected)
    form['name'] = 'new name'
    form['abbreviation'] = 'NEW'
    form.submit(status=302)
    assert proposition_type.name == 'new name'
    assert proposition_type.abbreviation == 'NEW'
