import argparse
import csv
from itertools import takewhile

from eliot import log_call, Message, start_action
import transaction
import sqlalchemy.orm


@log_call
def load_and_organize(filepath, voting_phase, log_level="INFO"):

    with open(filepath) as csvfile:
        with start_action(log_level="INFO", action_type="load_csv"):
            reader = csv.reader(csvfile)
            rows = list(reader)

    for row_number, row in enumerate(rows):
        with start_action(log_level="INFO", action_type="organize_row"):
            Message.log(row_number=row_number + 1, row=row)
            head_proposition = (session.query(Proposition)
                                .filter_by(voting_identifier=row[0].strip())
                                .join(Ballot)
                                .join(VotingPhase)
                                .filter_by(name=voting_phase)).one()

            tail_row = [identifier.strip() for identifier in row[1:]]
            tail_propositions = (session.query(Proposition)
                                 .filter(Proposition.voting_identifier.in_(tail_row))
                                 .join(Ballot)
                                 .join(VotingPhase)
                                 .filter_by(name=voting_phase)).all()

            Message.log(_msg="found propositions",
                        head_proposition=head_proposition.voting_identifier,
                        tail_propositions=[p.voting_identifier for p in tail_propositions])
            head_ballot = head_proposition.ballot
            for proposition in tail_propositions:
                proposition.ballot = head_ballot
            head_proposition.replacements = tail_propositions


@log_call
def fixup_ballots(voting_phase, log_level="INFO"):
    ballots = (session.query(Ballot)
               .join(VotingPhase)
               .filter_by(name=voting_phase))
    deleted_ballots = []
    modified_ballots = []
    for ballot in ballots:
        with start_action(log_level="INFO", action_type="fixup_ballot"):
            if ballot.propositions:
                new_name = ballot_name(ballot.propositions[0], ballot.propositions[1:])
                if ballot.name != new_name:
                    modified_ballots.append({"before": ballot.name, "new": new_name})
                    ballot.name = new_name
            else:
                deleted_ballots.append(ballot.name or ballot.id)
                session.delete(ballot)

    return dict(modified_ballots=modified_ballots, deleted_ballots=deleted_ballots)


def longest_common_prefix_len(strings):
    return len(list(takewhile((lambda chars: len(set(chars)) == 1), zip(*strings))))


@log_call
def ballot_name(head_proposition, tail_propositions, log_level="INFO"):
    if tail_propositions:
        prefix_len = longest_common_prefix_len(p.voting_identifier for p in tail_propositions)
        shortened = "/".join(p.voting_identifier[prefix_len-1:] for p in tail_propositions)
        return (head_proposition.voting_identifier + "/" + shortened)[:63]
    else:
        return head_proposition.voting_identifier


parser = argparse.ArgumentParser("Ekklesia Portal organize_ballots.py")
parser.add_argument("-c", "--config-file", help=f"path to config file in YAML / JSON format")
parser.add_argument("-v", "--voting-phase", help=f"Choose the voting phase to organize from.")
parser.add_argument("-f", "--filepath", help=f"Choose the filepath to organize from.")


if __name__ == "__main__":
    args = parser.parse_args()

    from ekklesia_portal.app import make_wsgi_app

    app = make_wsgi_app(args.config_file)

    from ekklesia_portal.datamodel import Ballot, Proposition, VotingPhase
    from ekklesia_common.database import Session

    session = Session()

    sqlalchemy.orm.configure_mappers()

    load_and_organize(args.filepath, args.voting_phase)

    fixup_ballots(args.voting_phase)

    input("press Enter to commit changes to the database, or CTRL-C to abort...")

    transaction.commit()
