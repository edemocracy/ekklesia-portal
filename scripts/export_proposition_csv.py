import argparse
import csv

from ekklesia_common import md
from eliot import log_call, start_task, Message, write_traceback
import sqlalchemy.orm

from ekklesia_portal.lib.propositions import propositions_to_csv


@log_call
def load_propositions():
    department = session.query(Department).filter_by(name=args.department).one()

    maybe_voting_phase = [v for v in department.voting_phases if v.name == args.voting_phase]

    if not maybe_voting_phase:
        raise ValueError(f"Voting phase {args.voting_phase} not found!")

    voting_phase = maybe_voting_phase[0]

    ballots = voting_phase.ballots
    return [p for ballot in ballots for p in ballot.propositions]


parser = argparse.ArgumentParser("Ekklesia Portal export_proposition_csv.py")
parser.add_argument("-c", "--config-file", help=f"path to config file in YAML / JSON format")
parser.add_argument("-d", "--department", help=f"Choose the department to export from.")
parser.add_argument("-v", "--voting-phase", help=f"Choose the voting phase to export from.")
parser.add_argument("-o", "--out", help=f"Choose output file.")

if __name__ == "__main__":
    args = parser.parse_args()

    from ekklesia_portal.app import make_wsgi_app

    app = make_wsgi_app(args.config_file)

    from ekklesia_portal.datamodel import Department
    from ekklesia_common.database import Session

    session = Session()

    sqlalchemy.orm.configure_mappers()

    instance_name = app.settings.common.instance_name
    propositions = load_propositions()
    csv_text = propositions_to_csv(propositions, origin=instance_name)
    with open(args.out, 'w') as csvfile:
        csvfile.write(csv_text)
