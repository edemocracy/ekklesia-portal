from tests.helpers.webtest_helpers import get_session


def test_index(client):
    res = client.get("/")
    content = res.body.decode()
    assert content.startswith("<!DOCTYPE html5>")
    assert '<a href="http://localhost/p' in content


def test_change_language(app, client):
    res = client.post("/change_language", {'lang': 'de', 'myurl': '/'}, status=302)
    session = get_session(app, client)
    assert session['lang'] == 'de'


def test_change_language_url_with_params(app, client):
    res = client.post("/change_language", {'lang': 'en', 'myurl': '/fromurl?param=yes&param2=no'}, status=302)
    assert res.headers['Location'] == 'http://localhost/fromurl?param=yes&param2=no'


def test_change_language_invalid(app, client):
    client.post("/change_language", {'lang': 'invalid'}, status=400)
