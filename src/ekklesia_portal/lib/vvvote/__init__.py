import json
from eliot import start_action
import requests

class VVVoteAPIException(Exception):
    pass


def create_election_in_vvvote(module_config, election_config):

    for url in module_config["api_urls"]:

        with start_action(action_type="post_election_config",
            election_config=election_config) as action:

            response = requests.post(f"{url}/newelection", data=election_config)
            response.raise_for_status()
            try:
                response_json = response.json()
            except json.JSONDecodeError:
                # VVVote may respond with HTML instead of JSON if something is wrong.
                raise VVVoteAPIException(response.text.replace("\n", " "))

            action.add_success_fields(response=response_json)

    return response_json["configUrl"]
