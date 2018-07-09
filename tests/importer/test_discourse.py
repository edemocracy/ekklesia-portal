import json
import responses
from ekklesia_portal.importer.discourse import import_discourse_post_as_proposition


TOPIC = {
    'title': 'title'
}


POST = {
    'raw': 'post content',
    'topic_id': 2
}


@responses.activate
def test_import_discourse_post_as_proposition():
    base_url = 'http://discourse-test'
    responses.add(responses.GET, base_url + '/posts/1', body=json.dumps(POST))
    responses.add(responses.GET, base_url + '/t/2', body=json.dumps(TOPIC))
    res = import_discourse_post_as_proposition(base_url, 1)
    expected = {
        'title': TOPIC['title'],
        'content': POST['raw']
    }
    assert res == expected
