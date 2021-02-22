from assert_helpers import assert_difference, assert_no_difference
from ekklesia_portal.datamodel import ArgumentRelation, ArgumentVote
from ekklesia_portal.enums import ArgumentType
from webtest_helpers import assert_deform


def test_argumentrelation(client, argument_relation):
    proposition = argument_relation.proposition
    argument = argument_relation.argument
    res = client.get(f"/p/{proposition.id}/a/{argument.id}")
    assert 'argument_vote_btn' not in res, 'vote button not present'
    html = res.html
    proposition_title_link = html.find(class_="proposition_title").find("a")
    assert proposition_title_link.text == proposition.title
    assert str(proposition.id) in proposition_title_link["href"]
    assert html.find(class_="argument_title").find("a").text == argument.title
    assert html.find(class_="argument_abstract").text == argument.abstract
    assert html.find(class_="argument_details_extended").text == argument.details


def test_argumentrelation_with_logged_in_user(client, argument_relation, logged_in_user):
    proposition = argument_relation.proposition
    argument = argument_relation.argument
    res = client.get(f"/p/{proposition.id}/a/{argument.id}")
    assert 'argument_vote_btn' in res, 'vote button present'


def test_new(client, logged_in_user, proposition):
    res = client.get(f'/p/{proposition.id}/a/+new?relation_type={ArgumentType.PRO.name}')

    expected = {'proposition_id': proposition.id, 'relation_type': ArgumentType.PRO.name}
    assert_deform(res, expected)


def test_create(db_query, client, logged_in_user, proposition):
    data = {
        'proposition_id': proposition.id,
        'relation_type': ArgumentType.PRO.name,
        'title': 'test title',
        'abstract': 'test abstract',
        'details': 'test details'
    }

    with assert_difference(db_query(ArgumentRelation).count, 1):
        client.post(f"/p/{proposition.id}/a/", data, status=302)


def test_does_not_create_without_title(db_query, client, logged_in_user, proposition):
    data = {
        'proposition_id': proposition.id,
        'relation_type': ArgumentType.PRO.name,
        'abstract': 'test abstract',
        'details': 'test details'
    }

    with assert_no_difference(db_query(ArgumentRelation).count):
        client.post(f"/p/{proposition.id}/a/", data, status=200)


def test_vote(db_query, client, logged_in_user, argument_relation):
    url = f"/p/{argument_relation.proposition_id}/a/{argument_relation.argument_id}/vote"
    client.post(url, {'weight': 1}, status=302)
    qq = db_query(ArgumentVote).filter_by(member_id=logged_in_user.id, relation_id=argument_relation.id).one
    vote = qq()
    assert vote.weight == 1

    client.post(url, {'weight': 0}, status=302)
    vote = qq()
    assert vote.weight == 0

    client.post(url, {'weight': -1}, status=302)
    vote = qq()
    assert vote.weight == -1

    client.post(url, {'weight': -2}, status=400)
    vote = qq()
    assert vote.weight == -1
