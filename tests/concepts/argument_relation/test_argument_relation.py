from webtest_helpers import assert_deform
from assert_helpers import assert_difference, assert_no_difference
from ekklesia_portal.datamodel import ArgumentVote, ArgumentRelation
from ekklesia_portal.enums import ArgumentType


def test_argumentrelation(client):
    """XXX: depends on content from create_test_db.py"""
    res = client.get("/propositions/1/arguments/3")
    content = res.body.decode()
    assert content.startswith("<!DOCTYPE html5>")
    assert 'argument_vote_btn' not in content
    assert 'Ein Titel' in content  # proposition title
    # argument
    assert 'Ein Contra-Argument' in content, 'argument title'
    assert 'dagegen' in content, 'argument abstract'
    assert 'aus Gründen' in content, 'argument details'


def test_argumentrelation_with_logged_in_user(client, logged_in_user):
    """XXX: depends on content from create_test_db.py"""
    res = client.get("/propositions/1/arguments/3")
    content = res.body.decode()
    assert 'argument_vote_btn' in content


def test_new(client, logged_in_user):
    res = client.get(f'/propositions/1/arguments/+new?relation_type={ArgumentType.PRO.name}')

    expected = {
        'proposition_id': '1',
        'relation_type': ArgumentType.PRO.name
    }
    assert_deform(res, expected)


def test_create(db_query, client, logged_in_user):
    data = {
        'proposition_id': 1,
        'relation_type': ArgumentType.PRO.name,
        'title': 'test title',
        'abstract': 'test abstract',
        'details': 'test details'
    }

    with assert_difference(db_query(ArgumentRelation).count, 1):
        client.post("/propositions/1/arguments/", data, status=302)


def test_does_not_create_without_title(db_query, client, logged_in_user):
    data = {
        'proposition_id': 1,
        'relation_type': ArgumentType.PRO.name,
        'abstract': 'test abstract',
        'details': 'test details'
    }

    with assert_no_difference(db_query(ArgumentRelation).count):
        client.post("/propositions/1/arguments/", data, status=200)


def test_vote(db_query, client, logged_in_user):
    client.post("/propositions/1/arguments/3/vote", {'weight': 1}, status=302)
    qq = db_query(ArgumentVote).filter_by(member_id=logged_in_user.id, relation_id=3).one
    vote = qq()
    assert vote.weight == 1

    client.post("/propositions/1/arguments/3/vote", {'weight': 0}, status=302)
    vote = qq()
    assert vote.weight == 0

    client.post("/propositions/1/arguments/3/vote", {'weight': -1}, status=302)
    vote = qq()
    assert vote.weight == -1

    client.post("/propositions/1/arguments/3/vote", {'weight': -2}, status=400)
    vote = qq()
    assert vote.weight == -1
