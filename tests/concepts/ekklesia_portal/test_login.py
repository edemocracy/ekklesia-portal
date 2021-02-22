from munch import Munch
from pytest import raises

from ekklesia_portal.concepts.ekklesia_portal.login import Login
from tests.helpers.webtest_helpers import get_session


def test_show_login(client):
    res = client.get("/login?internal_login=1")
    assert "Username" in res
    assert "username" in res


def test_submit_login(app, client):
    res = client.post("/login", dict(username="testuser", password="test"), status=302)
    session = get_session(app, client)
    assert "user_id" in session


def test_submit_login_wrong_password(app, client):
    res = client.post("/login", dict(username="testuser", password="wrong"), status=200)
    assert res.headers["Set-Cookie"].startswith("session=;")


def test_submit_login_incomplete(client):
    client.post("/login", dict(username="testuser"), status=400)


def test_find_user_with_wrong_username(req):
    login = Login(request=req, username='invalid', password='')
    assert not login.find_user()


def test_verify_password_without_user_raises_value_error():
    login = Login()
    with raises(ValueError):
        login.verify_password(False)


def test_verify_password_is_false_when_user_pw_is_none():
    login = Login()
    login.user = Munch(password=None)
    assert login.verify_password(False) is False


def test_verify_password_is_true_for_empty_pw_with_insecure_mode():
    login = Login(username='test', password='')
    login.user = Munch(password='pw')
    assert login.verify_password(True) is True
