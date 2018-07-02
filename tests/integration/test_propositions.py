import pytest
from webtest_helpers import assert_deform

@pytest.mark.integration
def test_user_creates_proposition(client):
    res = client.get('/propositions/+new')
    form = res.forms['deform']
    assert form.action.endswith('propositions')

    form['title'] = 'test title'
    form['short'] = 'short'
    form['content'] = 'test content'

    # user should be redirected and see new proposition
    res = form.submit(status=302)
    res = res.follow()
    content = res.body.decode()
    assert 'test content' in content

    # user should see the proposition on the index page
    res = client.get('/propositions')
    content = res.body.decode()
    assert 'test title' in content
