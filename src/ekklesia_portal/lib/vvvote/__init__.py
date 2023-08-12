import json
from eliot import start_action
import requests
import ekklesia_portal.lib.vvvote.schema as vvvote_schema


class VVVoteAPIException(Exception):
    pass


def create_election_in_vvvote(module_config, election_config) -> str:

    for url in module_config["api_urls"]:

        with start_action(
            action_type="post_election_config", election_config=election_config
        ) as action:

            response = requests.post(f"{url}/newelection", data=election_config)
            response.raise_for_status()
            try:
                response_json = response.json()
            except json.JSONDecodeError:
                # VVVote may respond with HTML instead of JSON if something is wrong.
                raise VVVoteAPIException(response.text.replace("\n", " "))

            cmd = response_json.get('cmd')

            if cmd == "error":
                raise VVVoteAPIException(f"error from vvvote: {response_json['errorNo']}: {response_json['errorTxt']}")
            elif cmd == 'saveElectionUrl':
                action.add_success_fields(response=response_json)
                break
            else:
                raise VVVoteAPIException(f"unexpected response from vvvote: {response}")

    config_url = response_json["configUrl"]
    return config_url


def retrieve_results_from_vvvote(module_config, voting_data):

    election_url = voting_data["config_url"]

    for url in module_config["api_urls"]:

        with start_action(action_type="retrieve_election_results", election_url=election_url) as action:
            response = requests.post(f"{election_url}&api=")
            response.raise_for_status()
            try:
                response_json = response.json()
            except json.JSONDecodeError:
                # VVVote may respond with HTML instead of JSON if something is wrong.
                raise VVVoteAPIException(response.text.replace("\n", " "))

            cmd = response_json.get('cmd')

            if cmd == "error":
                raise VVVoteAPIException(f"error from vvvote: {response_json['errorNo']}: {response_json['errorTxt']}")
            elif cmd == 'loadElectionConfig':
                election_id = response_json.get("electionId")
            else:
                raise VVVoteAPIException(f"unexpected response from vvvote: {response}")

            response = requests.post(f"{url}/getresult", data=json.dumps({"cmd": "getWinners", "electionId": election_id}))
            response.raise_for_status()
            try:
                response_json = response.json()
            except json.JSONDecodeError:
                # VVVote may respond with HTML instead of JSON if something is wrong.
                raise VVVoteAPIException(response.text.replace("\n", " "))

            cmd = response_json.get('cmd')

            if cmd == "error":
                raise VVVoteAPIException(f"error from vvvote: {response_json['errorNo']}: {response_json['errorTxt']}")
            elif cmd == 'showWinners':
                action.add_success_fields(response=response_json)
                break
            else:
                raise VVVoteAPIException(f"unexpected response from vvvote: {response}")

    return response_json["data"]
