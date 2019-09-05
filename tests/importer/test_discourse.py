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
    post_url = base_url + '/posts/1'
    topic_url = base_url + '/t/2'
    responses.add(responses.GET, post_url, body=json.dumps(POST))
    responses.add(responses.GET, topic_url, body=json.dumps(TOPIC))
    res = import_discourse_post_as_proposition(base_url, 1)
    expected = {
        'title': TOPIC['title'],
        'content': POST['raw'],
        'external_discussion_url': topic_url
    }
    assert res == expected
