def test_show_login(client):
    res = client.get("/login")
    content = res.body.decode()
    assert content.startswith("<!DOCTYPE html5>")
    assert "Username" in content
    assert "username" in content


def test_submit_login(client):
    res = client.post("/login", dict(username="testuser", password="test"), status=302)
    assert "Set-Cookie" in res.headers
    assert res.headers["Set-Cookie"].startswith("session=")


def test_submit_login_wrong_password(client):
    res = client.post("/login", dict(username="testuser", password="wrong"), status=200)
    content = res.body.decode()
    assert "testuser" in content
    assert "Set-Cookie" not in res.headers


def test_submit_login_incomplete(client):
    client.post("/login", dict(username="testuser"), status=400)
