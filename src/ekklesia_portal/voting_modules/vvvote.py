from eliot import start_action

from ekklesia_portal.datamodel import VotingPhase
from ekklesia_portal.lib.vvvote import create_election_in_vvvote, retrieve_results_from_vvvote
from ekklesia_portal.lib.vvvote.election_config import voting_phase_to_vvvote_election_config


def create_vvvote_voting(module_config: dict, voting_phase: VotingPhase) -> dict:

    with start_action(action_type="create_vvvote_election_config", module_config=module_config, voting_phase=voting_phase):
        election_config = voting_phase_to_vvvote_election_config(module_config, voting_phase).to_json()

    with start_action(action_type="create_election_in_vvvote", election_config=election_config) as action:
        config_url = create_election_in_vvvote(module_config, election_config)
        action.add_success_fields(config_url=config_url)

    return {"config_url": config_url, "results_url": config_url + "&showresult"}


def retrieve_vvvote_voting(module_config: dict, voting_data: str) -> dict:

    with start_action(action_type="retrieve_election_from_vvvote") as action:
        results = retrieve_results_from_vvvote(module_config, voting_data)
        action.add_success_fields(results=results)

    return results
