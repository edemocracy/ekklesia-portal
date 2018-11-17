import pytest


@pytest.mark.integration
def test_user_creates_proposition(client, logged_in_user_with_departments):
    user = logged_in_user_with_departments
    res = client.get('/p/+new')
    form = res.forms['deform']
    assert form.action.endswith('p')

    form['title'] = 'test title'
    form['abstract'] = 'abstract'
    form['content'] = 'test content'
    form['area_id'] = user.departments[0].areas[0].id

    # user should be redirected and see new proposition
    res = form.submit(status=302)
    res = res.follow()
    content = res.body.decode()
    assert 'test content' in content

    # user should see the proposition on the index page
    res = client.get('/p')
    content = res.body.decode()
    assert 'test title' in content
