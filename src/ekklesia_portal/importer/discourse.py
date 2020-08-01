import re

import requests


def parse_raw_content(raw: str):
    subsection_pattern = '((?:[^#]|#{3,})+)'
    abstract_header = '^## (?:(?:Zusammenfassung)|(?:Abstract))\n+'
    content_header = '^## (?:(?:Proposition)|(?:Antrag))\n+'
    motivation_header = '^## (?:(?:Motivation)|(?:Begründung))\n+'

    abstract_match = re.search(abstract_header + subsection_pattern, raw, re.MULTILINE)
    content_match = re.search(content_header + subsection_pattern, raw, re.MULTILINE)
    motivation_match = re.search(motivation_header + subsection_pattern, raw, re.MULTILINE)

    return {
        'abstract': abstract_match.group(1).strip() if abstract_match else None,
        'content': content_match.group(1).strip() if content_match else None,
        'motivation': motivation_match.group(1).strip() if motivation_match else None
    }


def import_discourse_post_as_proposition(base_url: str, from_data):
    post_id = int(from_data)
    post_url = f"{base_url}/posts/{post_id}"

    res = requests.get(post_url, headers=dict(Accept="application/json"))
    post_data = res.json()

    raw = post_data.get("raw")
    if raw is None:
        raise ValueError("malformed discourse post JSON, key 'raw' not found!")

    parsed_content = parse_raw_content(raw)

    topic_id = post_data.get("topic_id")
    if topic_id is None:
        raise ValueError("malformed discourse post JSON, key 'topic_id' not found!")

    topic_url = f"{base_url}/t/{topic_id}"
    res = requests.get(topic_url, headers=dict(Accept="application/json"))
    topic_data = res.json()

    title = topic_data.get("title")
    if title is None:
        raise ValueError("malformed discourse topic JSON, key 'title' not found!")

    return {'title': title, 'external_discussion_url': topic_url, **parsed_content}
