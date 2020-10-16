from ekklesia_portal.datamodel import VotingPhase
from ekklesia_portal.lib.vvvote.election_config import voting_phase_to_vvvote_election_config


def create_vvvote_voting(module_config: dict, voting_phase: VotingPhase):
    election_config = voting_phase_to_vvvote_election_config(module_config, voting_phase).to_json()
    create_election_in_vvvote(module_config, election_config)

