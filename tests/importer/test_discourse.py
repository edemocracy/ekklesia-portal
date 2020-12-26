import json

import responses

from ekklesia_portal.importer.discourse import import_discourse_post_as_proposition, parse_raw_content

ABSTRACT = 'This is an abstract.'
CONTENT = 'We want...'
MOTIVATION = '''Start

### Reason 1

### Reason 2

End'''

RAW = f'''
## Zusammenfassung

{ABSTRACT}

## Antragstext

{CONTENT}

## Begründung

{MOTIVATION}
'''

TOPIC = {'title': 'title'}

POST = {'raw': RAW, 'topic_id': 2}

EXPECTED_PARSED_CONTENT = {'abstract': ABSTRACT, 'content': CONTENT, 'motivation': MOTIVATION, 'all_matched': True}


def test_parse_raw_content():
    parsed_content = parse_raw_content(RAW)
    assert parsed_content == EXPECTED_PARSED_CONTENT


@responses.activate
def test_import_discourse_post_as_proposition():
    base_url = 'http://discourse-test'
    post_url = base_url + '/posts/1'
    topic_url = base_url + '/t/2'
    responses.add(responses.GET, post_url, body=json.dumps(POST))
    responses.add(responses.GET, topic_url, body=json.dumps(TOPIC))
    res = import_discourse_post_as_proposition(dict(base_url=base_url), 1)
    expected = {'title': TOPIC['title'], 'external_discussion_url': topic_url, **EXPECTED_PARSED_CONTENT}
    assert res == expected
