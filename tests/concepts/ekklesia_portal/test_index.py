from tests.helpers.webtest_helpers import get_session


def test_index(client):
    res = client.get("/")
    content = res.body.decode()
    assert content.startswith("<!DOCTYPE html5>")
    assert '<a href="http://localhost/propositions' in content


def test_change_language(app, client):
    client.post("/change_language", {'lang': 'de'})
    session = get_session(app, client)
    assert session['lang'] == 'de'

    client.post("/change_language", {'lang': 'fr'})
    session = get_session(app, client)
    assert session['lang'] == 'fr'

    client.post("/change_language", {'lang': 'invalid'}, status=400)
