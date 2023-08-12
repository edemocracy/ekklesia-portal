from .vvvote import create_vvvote_voting, retrieve_vvvote_voting

# A voting modules consists of two functions with the following signatures:
# def create_voting(voting_module_config: dict, voting_phase: VotingPhase)
# def retrieve_voting(voting_module_config: dict, module_data: str)
#   where `voting_module_config` is the config returned by `prepare_module_config`
#   and `module_data` is the return value of `create_config`.
# Return values:
# create_voting: {"config_url": config_url, "results_url": results_url}
#   where `config_url` is the link to show the user for registration and
#   `results_url` is the link to show the user after voting has finished.
# retrieve_voting: {"1": [2,3]}
#   where 1 is the enumerated id of one of many ballot ids and 2,3 are the enumerated ids of all accepted propositions in this ballot.
VOTING_MODULES = {
    "vvvote": (create_vvvote_voting, retrieve_vvvote_voting)
}
