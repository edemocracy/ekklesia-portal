from eliot import start_action
from dataclasses import dataclass
from typing import List

import requests
from requests import HTTPError


@dataclass
class DiscourseTopic:
    content: str
    title: str
    tags: List[str]


@dataclass
class DiscourseConfig:
    api_key: str
    api_username: str
    base_url: str
    category: int


class DiscourseError(Exception):
    pass


def create_discourse_topic(config: DiscourseConfig, topic: DiscourseTopic, with_tags: bool = True):

    headers = {'accept': 'application/json', 'api-key': config.api_key, 'api-username': config.api_username}

    if with_tags:
        req = {'raw': topic.content, 'category': config.category, 'title': topic.title, 'tags': topic.tags}
    else:
        req = {'raw': topic.content, 'category': config.category, 'title': topic.title}

    with start_action(action_type="discourse_post", with_tags=with_tags) as action:
        resp = requests.post(f"{config.base_url}/posts.json", json=req, headers=headers)
        action.add_success_fields(response=resp.json())

    try:
        resp.raise_for_status()
    except HTTPError as e:
        if e.response.status_code == 422 and with_tags:
            # Try again once without tags
            return create_discourse_topic(config, topic, with_tags=False)
        else:
            raise DiscourseError(e)

    return resp
