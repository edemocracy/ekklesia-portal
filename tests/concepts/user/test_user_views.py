from webtest_helpers import assert_deform


def test_show(db_session, client, logged_in_user):
    user = logged_in_user
    res = client.get(f'/u/{user.name}')
    assert user.name in res


def test_update(db_session, client, user, group, logged_in_global_admin):
    res = client.get(f'/u/{user.name}/+edit')
    form = assert_deform(res)
    form['groups'] = [group.name]
    form.submit(status=302)
    assert [g.name for g in user.groups] == [group.name]


def test_update_not_allowed_for_anon(db_session, client, user):
    res = client.get(f'/u/{user.name}/+edit', status=302)
    assert "/login" in res.location
    res = client.post(f'/u/{user.name}', status=302)
    assert "/login" in res.location


def test_update_not_allowed_for_normal_user(db_session, client, user, logged_in_user):
    client.get(f'/u/{user.name}/+edit', status=403)
    client.post(f'/u/{user.name}', status=403)


def test_cannot_view_profile_of_another_user(db_session, client, logged_in_user, user_two):
    client.get(f'/u/{user_two.name}', status=403)


def test_admin_can_view_profile_of_another_user(db_session, client, logged_in_global_admin, user):
    client.get(f'/u/{user.name}')
