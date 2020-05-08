import factory
from webtest_helpers import assert_deform, fill_form
from assert_helpers import assert_difference, assert_no_difference
from ekklesia_portal.database.datamodel import BallotVoting


def test_create_ballot_voting(client, db_query, ballot_voting_factory):
    data = factory.build(dict, FACTORY_CLASS=ballot_voting_factory)
    res = client.get('/ballot_votings/+new')
    form = assert_deform(res)
    fill_form(form, data, ['name'])

    with assert_difference(db_query(BallotVoting).count, 1):
        form.submit(status=302)


def test_update_ballot_voting(db_session, client, ballot_voting_factory):
    ballot_voting = ballot_voting_factory()
    res = client.get(f'/ballot_votings/{ ballot_voting.id}/+edit')
    expected = ballot_voting.to_dict()
    form = assert_deform(res, expected)
    form['name'] = 'new name'
    form.submit(status=302)
    assert ballot_voting.name == 'new name'
