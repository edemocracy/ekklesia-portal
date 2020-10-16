from eliot import start_action
import requests

def create_election_in_vvvote(module_config, election_config):

    for url in module_config["api_urls"]:

        with start_action(action_type="post_election_config") as action:
            resp = requests.post(f"{url}/newelection", data=election_config)
            resp.raise_for_status()
            action.add_success_fields(response=resp.json())

    return resp.json()["configUrl"]
