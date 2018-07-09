import requests


def import_discourse_post_as_proposition(base_url, from_data):
    post_id = int(from_data)
    post_url = "{}/posts/{}".format(base_url, post_id)

    res = requests.get(post_url, headers=dict(Accept="application/json"))
    post_data = res.json()

    content = post_data.get("raw")
    if content is None:
        raise ValueError("malformed discourse post JSON, key 'raw' not found!")

    topic_id = post_data.get("topic_id")
    if topic_id is None:
        raise ValueError("malformed discourse post JSON, key 'topic_id' not found!")

    topic_url = "{}/t/{}".format(base_url, topic_id)
    res = requests.get(topic_url, headers=dict(Accept="application/json"))
    topic_data = res.json()

    title = topic_data.get("title")
    if title is None:
        raise ValueError("malformed discourse topic JSON, key 'title' not found!")

    return {
        'title': title,
        'content': content
    }
