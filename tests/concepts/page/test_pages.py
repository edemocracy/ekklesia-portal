import factory
from ekklesia_common import md

from assert_helpers import assert_difference, assert_no_difference
from ekklesia_portal.datamodel import Page
from webtest_helpers import assert_deform, fill_form


def test_page(client, db_query, page_factory):
    page = page_factory()
    res = client.get(f'/pages/{page.name}/{page.lang}')

    expected = md.convert(page.text)
    assert expected in res


def test_create_page(client, db_query, page_factory, logged_in_global_admin):
    data = factory.build(dict, FACTORY_CLASS=page_factory)
    res = client.get('/pages/+new')
    form = assert_deform(res)
    fill_form(form, data, ['name', 'lang', 'title', 'text'])

    with assert_difference(db_query(Page).count, 1):
        form.submit(status=302)


def test_update_page(db_session, client, page_factory, logged_in_global_admin):
    page = page_factory()
    res = client.get(f'/pages/{page.name}/{page.lang}/+edit')
    expected = page.to_dict()
    form = assert_deform(res, expected)
    form['text'] = 'new text'
    form.submit(status=302)
    assert page.text == 'new text'
