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


def _set_form_field_value(form, data, field_name, enum_field_names):
    if field_name in enum_field_names:
        value = data[field_name].name
    else:
        value = data[field_name]

    form.set(field_name, value)


def fill_form(form, data, field_names=None, enum_field_names=[]):
    if field_names is None:
        for field_name in data:
            _set_form_field_value(form, data, field_name, enum_field_names)
    else:
        for field_name in field_names:
            _set_form_field_value(form, data, field_name, enum_field_names)

    return form
