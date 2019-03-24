import factory
from webtest_helpers import assert_deform, fill_form
from assert_helpers import assert_difference, assert_no_difference
from {{ cookiecutter.app_name }}.database.datamodel import {{ cookiecutter.ConceptName }}


def test_create_{{ cookiecutter.concept_name }}(client, db_query, {{ cookiecutter.concept_name }}_factory):
    data = factory.build(dict, FACTORY_CLASS={{cookiecutter.concept_name}}_factory)
    res = client.get('/{{cookiecutter.concept_names}}/+new')
    form = assert_deform(res)
    fill_form(form, data, ['name'])

    with assert_difference(db_query({{ cookiecutter.ConceptName }}).count, 1):
       form.submit(status=302)


def test_update_{{ cookiecutter.concept_name }}(db_session, client, {{ cookiecutter.concept_name }}_factory):
    {{ cookiecutter.concept_name }} = {{ cookiecutter.concept_name }}_factory()
    res = client.get(f'/{{cookiecutter.concept_names}}/{{ "{" }} {{ cookiecutter.concept_name }}.id{{ "}" }}/+edit')
    expected = {{ cookiecutter.concept_name }}.to_dict()
    form = assert_deform(res, expected)
    form['name'] = 'new name'
    form.submit(status=302)
    assert {{ cookiecutter.concept_name }}.name == 'new name'
