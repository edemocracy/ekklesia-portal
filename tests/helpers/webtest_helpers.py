def assert_deform(response, expected_form_data):
    assert 'deform' in response.forms
    form = response.forms['deform']

    for field, value in expected_form_data.items():
        assert form[field].value == value


def get_session(app, client):
    serializer = app.browser_session_interface.get_signing_serializer(app)
    assert 'session' in client.cookies
    return serializer.loads(client.cookies['session'])
