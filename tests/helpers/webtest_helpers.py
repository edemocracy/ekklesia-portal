from enum import Enum


def python_to_deform_value(py_value):
    if py_value is True:
        return 'true'
    elif py_value is False:
        return 'false'
    elif py_value is None:
        return ''
    elif isinstance(py_value, Enum):
        return py_value.name
    else:
        return str(py_value)


def assert_deform(response, expected_form_data={}):
    assert 'deform' in response.forms
    form = response.forms['deform']

    for field, value in expected_form_data.items():
        if field == 'id':
            continue

        try:
            form_field = form[field]
        except AssertionError:
            raise AssertionError(f"expected form field '{field}' is missing")
        form_value = form[field].value

        deform_value = python_to_deform_value(value)
        assert form_value == deform_value, f'form field {field}: form value {form_value} != expected {deform_value}'

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
