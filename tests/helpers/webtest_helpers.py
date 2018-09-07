def python_to_deform_value(py_value):
    if py_value == True:
        return 'true'
    elif py_value == False:
        return 'false'
    else:
        return str(py_value)


def assert_deform(response, expected_form_data={}):
    assert 'deform' in response.forms
    form = response.forms['deform']

    for field, value in expected_form_data.items():
        if field == 'id':
            continue

        form_value = form[field].value
        assert form_value == python_to_deform_value(value), f'form field {field}: form value {form_value} != {value}'

    return form


def get_session(app, client):
    serializer = app.browser_session_interface.get_signing_serializer(app)
    assert 'session' in client.cookies
    return serializer.loads(client.cookies['session'])


def fill_form(form, data, field_names=None):
    if field_names is None:
        for field_name, value in data.items():
            form.set(field_name, value)
    else:
        for field_name in field_names:
            form.set(field_name, data[field_name])

    return form
