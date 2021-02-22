from assert_helpers import assert_difference, assert_no_difference
from ekklesia_portal.datamodel import User


def test_token(client, user_login_token_factory, page_factory):
    page = page_factory(name='content_token_login', lang='en', text='test text')
    token = user_login_token_factory()
    res = client.get("/token/" + token.token)
    assert "tos_consent" in res
    assert page.text in res


def test_token_wrong_token(db_query, client):
    client.get("/token/" + "1234", status=404)


def test_submit_token_new_user(db_query, client, user_login_token_factory):
    token = user_login_token_factory()

    with assert_difference(db_query(User).count, 1, 'user'):
        res = client.post("/token/" + token.token, dict(tos_consent='true'), status=302)

    assert "Set-Cookie" in res.headers
    assert res.headers["Set-Cookie"].startswith("session=")


def test_submit_token_existing_user(db_query, client, user_factory, user_login_token_factory):
    token = user_login_token_factory()
    user = user_factory(auth_type='token', login_token=token)

    with assert_no_difference(db_query(User).count, 'user'):
        res = client.post("/token/" + token.token, dict(tos_consent='true'), status=302)

    assert "Set-Cookie" in res.headers
    assert res.headers["Set-Cookie"].startswith("session=")


def test_submit_token_wrong_token(db_query, client):

    with assert_no_difference(db_query(User).count, 'user'):
        res = client.post("/token/" + "1234", dict(tos_consent='true'), status=404)

    assert "Set-Cookie" not in res.headers
