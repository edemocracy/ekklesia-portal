import datetime

import transaction
from typer import run
from typing import Optional

from datetime import datetime, timedelta

from ekklesia_common.database import Session
from ekklesia_portal.datamodel import Supporter, AreaMember, Proposition, VotingPhase, SubjectArea, Department, VotingPhaseType
from ekklesia_portal.enums import SupporterStatus, PropositionStatus, VotingStatus, VotingType


def cleanup_subject_area_members(session: Session):
    """
        "Der Status als Teilnehmer verfällt automatisch nach dem zweiten Stichtag
         nach der letzten solchen Anmeldung des Teilnehmers."
    """
    now = datetime.now()

    # Separate deadline for every department
    departments = session.query(Department).all()
    for department in departments:
        # Get second to last phase in current department of those which happened online and are already over
        phase = session.query(VotingPhase).join(VotingPhaseType) \
                .filter(VotingPhase.department == department,
                        VotingPhaseType.voting_type == VotingType.ONLINE,
                        VotingPhase.target < now) \
                .order_by(VotingPhase.target.desc()).limit(1).offset(1) \
                .first()

        # Only check here if there are at least two finished phases in this department
        if phase:
            cleanup_threshold = phase.target
            members = session.query(AreaMember).join(SubjectArea)\
                .filter(SubjectArea.department == department,
                        AreaMember.updated_at < cleanup_threshold)\
                .all()
            for member in members:
                print("Expiring", member.member_id, "'s area membership of", member.area_id)
                session.delete(member)


def cleanup_proposition_support(session: Session):
    """
        "Nach zwölf Wochen verfällt eine Unterstützung der Abstimmung des Antrags automatisch."
    """
    cleanup_threshold = datetime.now() - timedelta(weeks=12)
    supporters = session.query(Supporter).filter(Supporter.status == SupporterStatus.ACTIVE,
                                                 Supporter.last_change <= cleanup_threshold).all()
    for supporter in supporters:
        print("Expiring", supporter.member_id, "'s supporter state of", supporter.proposition_id)
        supporter.status = SupporterStatus.EXPIRED
        supporter.last_change = datetime.now()


def cleanup_stale_propositions(session: Session):
    """
        "Ein Antrag verfällt, [...] wenn er innerhalb von sechs Monaten das
        notwendige Quorum zur Zulassung zur Abstimmung nicht erreicht hat."
    """
    cleanup_threshold = datetime.now() - timedelta(days=30*6)
    propositions = session.query(Proposition).filter(Proposition.status == PropositionStatus.SUBMITTED,
                                                     Proposition.submitted_at <= cleanup_threshold).all()

    for proposition in propositions:
        print("Abandoning proposition", proposition.id)
        proposition.status = PropositionStatus.ABANDONED


def check_voting_phases(session: Session):
    """
    Change voting phase to VOTING or FINISHED if the deadlines have passed.
    Change state of all propositions attached to the voting phases to VOTING or FINISHED respectively.
    """
    voting_phases = session.query(VotingPhase).all()
    now = datetime.now()

    for voting_phase in voting_phases:
        # If phase was preparing but voting start time is in the past, set state to voting
        if voting_phase.status == VotingStatus.PREPARING and voting_phase.voting_start and voting_phase.voting_start <= now:
            print("Setting voting phase", voting_phase.id, "to VOTING")
            voting_phase.status = VotingStatus.VOTING

        # If phase was voting but voting start end is in the past, set state to finished
        if voting_phase.status == VotingStatus.VOTING and voting_phase.voting_end and voting_phase.voting_end <= now:
            print("Setting voting phase", voting_phase.id, "to FINISHED")
            voting_phase.status = VotingStatus.FINISHED

        # If voting phase is either voting or finished, check proposition states
        if voting_phase.status == VotingStatus.VOTING or voting_phase.status == VotingStatus.FINISHED:
            for ballot in voting_phase.ballots:
                for proposition in ballot.propositions:
                    # if phase is voting, update propositions to voting
                    if voting_phase.status == VotingStatus.VOTING and proposition.status != PropositionStatus.VOTING:
                        print("Setting proposition", proposition.id, "to VOTING")
                        proposition.status = PropositionStatus.VOTING
                    # if phase is finished, update propositions to finished
                    elif voting_phase.status == VotingStatus.FINISHED and proposition.status != PropositionStatus.FINISHED:
                        print("Setting proposition", proposition.id, "to FINISHED")
                        proposition.status = PropositionStatus.FINISHED


def main(config: Optional[str] = None):
    from ekklesia_portal.app import make_wsgi_app

    make_wsgi_app(config)
    session = Session()

    cleanup_subject_area_members(session)

    cleanup_proposition_support(session)

    cleanup_stale_propositions(session)

    check_voting_phases(session)

    transaction.commit()


if __name__ == "__main__":
    run(main)
