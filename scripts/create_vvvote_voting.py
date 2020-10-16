from typing import Optional
from typer import echo, run, Exit
import transaction
from ekklesia_common.database import Session
from ekklesia_portal.datamodel import VotingPhase
from ekklesia_portal.enums import VotingStatus
from ekklesia_portal.lib.voting import prepare_module_config
from ekklesia_portal.lib.vvvote.election_config import voting_phase_to_vvvote_election_config
from ekklesia_portal.lib.vvvote import create_election_in_vvvote


def main(voting_phase_name: str, voting_module_name: str, update_existing: Optional[bool] = False, out: Optional[str] = None, config: Optional[str] = None):
    from ekklesia_portal.app import make_wsgi_app

    app = make_wsgi_app(config)

    session = Session()

    voting_phase = session.query(VotingPhase).filter_by(name=voting_phase_name).one()
    department = voting_phase.department
    module_config = prepare_module_config(app, department, voting_module_name)

    election_config = voting_phase_to_vvvote_election_config(module_config, voting_phase).to_json()

    if out:
        with open(out, "w") as wf:
            wf.write(election_config)
    elif voting_module_name in voting_phase.voting_module_data and not update_existing:
        config_url = voting_phase.voting_module_data[voting_module_name]["config_url"]
        echo(f"VVVote voting already exists for this voting phase at {config_url}, doing nothing. Add --update-existing to create a new voting.")
    elif voting_phase.status != VotingStatus.SCHEDULED:
        echo(f"Voting can only be created for scheduled voting phases, this voting phase is in state '{voting_phase.status}'!")
        raise Exit(1)
    else:
        config_url = create_election_in_vvvote(module_config, election_config)
        voting_phase.voting_module_data[voting_module_name] = {"config_url": config_url}
        transaction.commit()
        echo(f"Created election config with id {config_url}.")


if __name__ == "__main__":
    run(main)
