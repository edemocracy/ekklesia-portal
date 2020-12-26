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


def create_discourse_topic(config: DiscourseConfig, topic: DiscourseTopic):

    headers = {'accept': 'application/json', 'api-key': config.api_key, 'api-username': config.api_username}

    req = {'raw': topic.content, 'category': config.category, 'title': topic.title, 'tags': topic.tags}

    with start_action(action_type="discourse_post") as action:
        resp = requests.post(f"{config.base_url}/posts.json", json=req, headers=headers)
        action.add_success_fields(response=resp.json())

    try:
        resp.raise_for_status()
    except HTTPError as e:
        raise DiscourseError(e)

    return resp
