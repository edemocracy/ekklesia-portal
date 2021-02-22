def test_show(db_session, client, logged_in_user):
    user = logged_in_user
    res = client.get(f'/u/{user.name}')
    assert user.name in res


def test_cannot_view_profile_of_another_user(db_session, client, logged_in_user, user_two):
    client.get(f'/u/{user_two.name}', status=403)
