import factory
from webtest_helpers import assert_deform, fill_form
from assert_helpers import assert_difference, assert_no_difference
from ekklesia_portal.database.datamodel import PropositionNote


def test_create_proposition_note(client, db_query, proposition_note_factory):
    data = factory.build(dict, FACTORY_CLASS=proposition_note_factory)
    res = client.get('/proposition_notes/+new')
    form = assert_deform(res)
    fill_form(form, data, ['name'])

    with assert_difference(db_query(PropositionNote).count, 1):
        form.submit(status=302)


def test_update_proposition_note(db_session, client, proposition_note_factory):
    proposition_note = proposition_note_factory()
    res = client.get(f'/proposition_notes/{ proposition_note.id}/+edit')
    expected = proposition_note.to_dict()
    form = assert_deform(res, expected)
    form['name'] = 'new name'
    form.submit(status=302)
    assert proposition_note.name == 'new name'
