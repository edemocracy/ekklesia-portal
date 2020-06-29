import argparse
import csv

from eliot import log_call, Message, start_action
import transaction
import sqlalchemy.orm


@log_call
def load_and_add_voting_result(filepath, voting_phase_name, log_level="INFO"):
    with open(filepath) as csvfile:
        with start_action(log_level="INFO", action_type="load_csv"):
            reader = csv.reader(csvfile)
            rows = list(reader)

    voting_phase = session.query(VotingPhase).filter_by(name=voting_phase_name).one()

    for row_number, row in enumerate(rows[1:]):
        with start_action(log_level="INFO", action_type="add_voting_result"):

            Message.log(data="current", row_number=row_number + 1, row=row)
            proposition = (session.query(Proposition)
                           .filter_by(voting_identifier=row[1].strip())
                           .join(Ballot)
                           .filter_by(voting=voting_phase)).one()

            Message.log(status="found proposition", proposition=proposition.voting_identifier)
            Message.log(data="before", row_number=row_number + 1, proposition_result=proposition.ballot.result)

            if not proposition.ballot.result:
                proposition.ballot.result = {}
            proposition.ballot.result[proposition.voting_identifier] = {'state': row[3].strip()}
            proposition.status = 'finished'

            Message.log(data="after", row_number=row_number + 1, proposition_result=proposition.ballot.result)


parser = argparse.ArgumentParser("Ekklesia Portal import_voting_result.py")
parser.add_argument("-c", "--config-file", help=f"path to config file in YAML / JSON format")
parser.add_argument("-v", "--voting-phase", help=f"Choose the voting phase to organize from.")
parser.add_argument("-f", "--filepath", help=f"Choose the filepath to import from.")

if __name__ == "__main__":
    args = parser.parse_args()

    from ekklesia_portal.app import make_wsgi_app

    app = make_wsgi_app(args.config_file)

    from ekklesia_portal.datamodel import Ballot, Proposition, VotingPhase
    from ekklesia_common.database import Session

    session = Session()
    session.autoflush = True

    sqlalchemy.orm.configure_mappers()

    load_and_add_voting_result(args.filepath, args.voting_phase)

    input("press Enter to commit changes to the database, or CTRL-C to abort...")

    transaction.commit()
