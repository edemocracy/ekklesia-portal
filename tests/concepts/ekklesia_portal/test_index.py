from tests.helpers.webtest_helpers import get_session


def test_index(client):
    res = client.get("/")
    assert '<a href="http://localhost/p' in res


def test_change_language(app, client):
    res = client.post("/change_language", {'lang': 'de', 'back_url': 'http://localhost/'}, status=302)
    session = get_session(app, client)
    assert session['lang'] == 'de'


def test_change_language_rejects_rouge_redirect(app, client):
    client.post("/change_language", {'lang': 'de', 'back_url': 'http://bad.example.com/'}, status=400)
    assert 'session' not in client.cookies


def test_change_language_url_with_params(app, client):
    res = client.post("/change_language", {'lang': 'en', 'back_url': 'http://localhost/fromurl?param=yes&param2=no'}, status=302)
    assert res.headers['Location'] == 'http://localhost/fromurl?param=yes&param2=no'


def test_change_language_invalid(app, client):
    client.post("/change_language", {'lang': 'invalid'}, status=400)
    assert 'session' not in client.cookies
