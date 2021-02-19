from tests.helpers.webtest_helpers import get_session


def test_logout(app, client):
    client.post("/login", dict(username="testuser", password="test"), status=302)
    client.post('/logout', status=302)
    session = get_session(app, client)
    assert "user_id" not in session
