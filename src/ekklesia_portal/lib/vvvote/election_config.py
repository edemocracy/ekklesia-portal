from datetime import datetime

import random
from uuid import uuid4

import ekklesia_portal.lib.vvvote.schema as vvvote_schema


def ballot_to_vvvote_question(ballot):
    options = []
    voting_scheme_yes_no = vvvote_schema.YesNoScheme(
        name=vvvote_schema.SchemeName.YES_NO, abstention=True, abstentionAsNo=False, quorum=2, mode=vvvote_schema.SchemeMode.QUORUM
    )

    proposition_count = len(ballot.propositions)
    voting_scheme_score = vvvote_schema.ScoreScheme(
        name=vvvote_schema.SchemeName.SCORE, minScore=0, maxScore=3 if proposition_count <= 5 else 9)

    voting_scheme = [voting_scheme_yes_no, voting_scheme_score]

    # Random order of propositions in ballot
    propositions = list(ballot.propositions)
    random.shuffle(propositions)

    for proposition in propositions:
        proponents = [s.member.name for s in proposition.propositions_member if s.submitter]
        option = vvvote_schema.Option(
            optionID=int(proposition.id) & ((2 ** 22) - 1),  # Only use the random bits (64bit not supported in JSON)
            proponents=proponents,
            optionTitle=proposition.title,
            optionDesc=proposition.content,
            reasons=proposition.motivation,
        )
        options.append(option)

    if len(ballot.propositions) == 1:
        question_wording = ballot.propositions[0].title
    else:
        question_wording = ballot.name

    question = vvvote_schema.Question(
        questionWording=question_wording,
        questionID=ballot.id,
        scheme=voting_scheme,
        options=options,
        findWinner=[vvvote_schema.SchemeName.YES_NO, vvvote_schema.SchemeName.SCORE, vvvote_schema.SchemeName.RANDOM]
    )

    return question


def get_ballot_sort_key(ballot):
    props = list(ballot.propositions)
    props.sort(key=lambda prop: prop.qualified_at or datetime.now())
    return props[0].qualified_at or datetime.now()


def voting_phase_to_vvvote_election_config(module_config, phase) -> vvvote_schema.ElectionConfig:
    ballots = list(phase.ballots)
    ballots.sort(key=get_ballot_sort_key)
    questions = [ballot_to_vvvote_question(ballot) for ballot in ballots]

    if phase.registration_start is None:
        raise ValueError("Cannot create voting for phase {phase}, registration_start is None")

    if phase.registration_end is None:
        raise ValueError("Cannot create voting for phase {phase}, registration_end is None")

    if phase.voting_start is None:
        raise ValueError("Cannot create voting for phase {phase}, voting_start is None")

    if phase.voting_end is None:
        raise ValueError("Cannot create voting for phase {phase}, voting_end is None")

    auth_data = vvvote_schema.OAuthConfig(
        eligible=module_config["must_be_eligible"],
        external_voting=True,
        verified=module_config["must_be_verified"],
        nested_groups=[module_config["required_role"]],
        serverId=module_config["auth_server_id"],
        RegistrationStartDate=phase.registration_start,
        RegistrationEndDate=phase.registration_end,
        VotingStart=phase.voting_start,
        VotingEnd=phase.voting_end,
    )
    config = vvvote_schema.ElectionConfig(
        electionId=str(uuid4()),
        electionTitle=phase.title or phase.name or phase.phase_type.name,
        tally=vvvote_schema.Tally.CONFIGURABLE,
        auth=vvvote_schema.Auth.OAUTH,
        authData=auth_data,
        questions=questions
    )
    return config
