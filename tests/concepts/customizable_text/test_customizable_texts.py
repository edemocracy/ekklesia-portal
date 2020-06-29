from ekklesia_common import md
import factory
from webtest_helpers import assert_deform, fill_form
from assert_helpers import assert_difference
from ekklesia_portal.datamodel import CustomizableText


def test_customizable_text(client, db_query, customizable_text_factory):
    customizable_text = customizable_text_factory()
    res = client.get(f'/customizable_texts/{customizable_text.name}/{customizable_text.lang}')
    content = res.body.decode()

    expected = md.convert(customizable_text.text)
    assert expected in content


def test_create_customizable_text(client, db_query, customizable_text_factory, logged_in_global_admin):
    data = factory.build(dict, FACTORY_CLASS=customizable_text_factory)
    res = client.get('/customizable_texts/+new')
    form = assert_deform(res)
    fill_form(form, data, ['name', 'lang', 'text'])

    with assert_difference(db_query(CustomizableText).count, 1):
        form.submit(status=302)


def test_update_customizable_text(db_session, client, customizable_text_factory, logged_in_global_admin):
    customizable_text = customizable_text_factory()
    res = client.get(f'/customizable_texts/{customizable_text.name}/{customizable_text.lang}/+edit')
    expected = customizable_text.to_dict()
    form = assert_deform(res, expected)
    form['text'] = 'new text'
    form.submit(status=302)
    assert customizable_text.text == 'new text'
