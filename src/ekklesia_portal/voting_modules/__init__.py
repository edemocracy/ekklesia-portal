from .vvvote import create_vvvote_voting

# import handlers are functions with the following signature:
# def import_handler(voting_module_config: dict, voting_phase: VotingPhase)
VOTING_MODULES = {
    "vvvote": create_vvvote_voting
}
