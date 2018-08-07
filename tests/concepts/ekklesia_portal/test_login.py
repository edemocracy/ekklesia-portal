from munch import Munch
from pytest import raises
from ekklesia_portal.concepts.ekklesia_portal.login import Login, UserNotFound


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


def test_find_user_with_wrong_username_raises_user_not_found(req):
    login = Login(request=req, username='invalid', password='')
    with raises(UserNotFound):
        login.find_user()


def test_verify_password_without_user_raises_value_error():
    login = Login()
    with raises(ValueError):
        login.verify_password(False)


def test_verify_password_is_false_when_user_pw_is_none():
    login = Login()
    login.user = Munch(password=None)
    assert login.verify_password(False) == False


def test_verify_password_is_true_for_empty_pw_with_insecure_mode():
    login = Login(username='test', password='')
    login.user = Munch(password='pw')
    assert login.verify_password(True) == True
