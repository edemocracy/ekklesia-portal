import argparse
import csv

import ekklesia_portal.helper.markdown as md
from eliot import log_call, start_task, Message, write_traceback
import sqlalchemy.orm


@log_call
def load_ballots(log_level="INFO"):
    department = session.query(Department).filter_by(name=args.department).one()

    maybe_voting_phase = [v for v in department.voting_phases if v.name == args.voting_phase]

    if not maybe_voting_phase:
        raise ValueError(f"Voting phase {args.voting_phase} not found!")

    voting_phase = maybe_voting_phase[0]

    ballots = voting_phase.ballots
    return ballots


@log_call
def convert_ballots_to_proposition_rows(ballots, log_level="INFO"):
    proposition_rows = []

    for ballot in ballots:
        for proposition in ballot.propositions:
            proposition_rows.append([proposition.id, "", proposition.title, md.convert(proposition.content),
                                     md.convert(proposition.motivation), "", "", "", "ekklesia-portal"])

    return proposition_rows


@log_call
def write_csv_file(filepath, proposition_rows, log_level="INFO"):
    with open(filepath, 'w') as csvfile:
        fieldnames = ['Identifier', 'Submitters', 'Title', 'Text', 'Reason', 'Category', 'Tags', 'Motion block', 'Origin']

        writer = csv.writer(csvfile)
        # maybe convert to dictwriter for better logging view

        writer.writerow(fieldnames)
        writer.writerows(proposition_rows)


parser = argparse.ArgumentParser("Ekklesia Portal export_proposition_csv.py")
parser.add_argument("-c", "--config-file", help=f"path to config file in YAML / JSON format")
parser.add_argument("-d", "--department", help=f"Choose the department to export from.")
parser.add_argument("-v", "--voting-phase", help=f"Choose the voting phase to export from.")
parser.add_argument("-o", "--out", help=f"Choose output file.")

if __name__ == "__main__":
    args = parser.parse_args()

    from ekklesia_portal.app import make_wsgi_app

    app = make_wsgi_app(args.config_file)

    from ekklesia_portal.database.datamodel import Department
    from ekklesia_portal.database import Session

    session = Session()

    sqlalchemy.orm.configure_mappers()

    write_csv_file(args.out, convert_ballots_to_proposition_rows(load_ballots()))
