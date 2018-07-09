def assert_deform(response, expected_form_data):
    assert 'deform' in response.forms
    form = response.forms['deform']

    for field, value in expected_form_data.items():
        assert form[field].value == value
