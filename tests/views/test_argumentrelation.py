from webtest_helpers import assert_deform

def test_argumentrelation(client):
    """XXX: depends on content from create_test_db.py"""
    res = client.get("/propositions/1/arguments/3")
    content = res.body.decode()
    assert content.startswith("<!DOCTYPE html5>")
    assert 'Ein Titel' in content  # proposition title
    # argument
    assert 'Ein Contra-Argument' in content, 'argument title'
    assert 'dagegen' in content, 'argument abstract'
    assert 'aus Gründen' in content, 'argument details'


def test_new(client, logged_in_user):
    res = client.get("/propositions/1/arguments/+new?relation_type=pro")
    form = res.forms['deform']

    expected = {
        'proposition_id': '1',
        'relation_type': 'pro'
    }
    assert_deform(res, expected)


def test_create(client, logged_in_user):
    data = {
        'proposition_id': 1,
        'relation_type': 'pro',
        'title': 'test title',
        'abstract': 'test abstract',
        'details': 'test details'
    }

    res = client.post("/propositions/1/arguments/", data, status=302)
