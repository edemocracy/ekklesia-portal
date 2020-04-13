from typing import List
from dataclasses import dataclass
import requests


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


def create_discourse_topic(config: DiscourseConfig, topic: DiscourseTopic):

    headers = {
        'accept': 'application/json',
        'api-key': config.api_key,
        'api-username': config.api_username
    }

    req = {
        'raw': topic.content,
        'category': config.category,
        'title': topic.title,
        'tags': topic.tags
    }

    resp = requests.post(f"{config.base_url}/posts.json", json=req, headers=headers)
    return resp

