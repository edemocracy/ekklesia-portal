from webtest_helpers import assert_deform

def test_index(client):
    """XXX: depends on content from create_test_db.py"""
    res = client.get("/propositions")
    content = res.body.decode()
    assert content.startswith("<!DOCTYPE html5>")
    assert 'Q1' in content


def test_new_with_data_import(client):
    from ekklesia_portal.importer import PROPOSITION_IMPORT_HANDLERS

    import_content = 'pre-filled content'
    import_title = 'pre-filled title'

    def import_test(base_url, from_data):
        if base_url == 'test' and from_data == '1':
            return dict(title=import_title, content=import_content)

    PROPOSITION_IMPORT_HANDLERS['test_source'] = import_test

    res = client.get('/propositions/+new?source=test&from_data=1')
    form = res.forms['deform']

    expected = {
        'title': 'pre-filled title',
        'content': 'pre-filled content'
    }
    assert_deform(res, expected)
