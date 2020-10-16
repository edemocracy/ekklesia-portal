import datetime
from ekklesia_portal.enums import VotingStatus
from ekklesia_portal.lib.vvvote.election_config import ballot_to_vvvote_question, voting_phase_to_vvvote_election_config


def test_ballot_to_vvvote_question(db_session, ballot, proposition_factory):
    proposition = proposition_factory(ballot=ballot)
    question = ballot_to_vvvote_question(ballot)
    assert question.questionID == 1
    assert question.options[0].optionTitle == proposition.title
    assert question.options[0].optionDesc == proposition.content
    assert question.options[0].reasons == proposition.motivation


def test_voting_phase_to_vvvote_election_config(db_session, ballot_factory, proposition_factory, voting_phase_factory):
    voting_phase = voting_phase_factory(status=VotingStatus.SCHEDULED, target=datetime.datetime.now())
    module_config = {
        "must_be_eligible": True,
        "must_be_verified": True,
        "required_role": "testrole",
        "auth_server_id": "testserver"
    }
    ballot_1 = ballot_factory()
    ballot_1.propositions = [proposition_factory(ballot=ballot_1)]
    ballot_2 = ballot_factory()
    ballot_2.propositions = [proposition_factory(ballot=ballot_2) for _ in range(3)]
    ballot_3 = ballot_factory()
    ballot_3.propositions = [proposition_factory(ballot=ballot_3) for _ in range(5)]
    voting_phase.ballots = [ballot_1, ballot_2, ballot_3]
    config = voting_phase_to_vvvote_election_config(module_config, voting_phase)
    assert len(config.electionId) == 36
    assert len(config.questions) == 3
    assert len(config.questions[0].options) == 1
    assert len(config.questions[1].options) == 3
    assert len(config.questions[2].options) == 5
