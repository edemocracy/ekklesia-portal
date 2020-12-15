import datetime
from dataclasses import asdict
from uuid import uuid4

from pytest import fixture

from ekklesia_portal.lib.vvvote.schema import (Auth, ElectionConfig, OAuthConfig, Option, Question, SchemeMode, ScoreScheme, Tally,
                                               YesNoScheme)


@fixture
def oauth_config():
    start_dt = datetime.datetime.now(datetime.timezone.utc)
    end_dt = start_dt + datetime.timedelta(days=4)

    return OAuthConfig(
        RegistrationStartDate=start_dt,
        RegistrationEndDate=end_dt,
        VotingStart=start_dt,
        VotingEnd=end_dt,
        eligible=True,
        external_voting=True,
        listId='abcddedbed',
        serverId='ekklesia',
        verified=True,
        nested_groups=['a', 'b']
    )


@fixture
def yes_no_scheme():
    return YesNoScheme(name='yesNo', abstention=True, abstentionAsNo=True, quorum=3, mode=SchemeMode.QUORUM)


@fixture
def score_scheme():
    return ScoreScheme(name='score', minScore=0, maxScore=3)


@fixture
def question(yes_no_scheme, score_scheme):

    option_1 = Option(
        optionID=1,
        proponents=['alice', 'bob'],
        optionTitle='Option 1',
        optionDesc='Desc for Option 1\nText',
    )

    option_2 = Option(
        optionID=2,
        proponents=['mallory'],
        optionTitle='Option 2',
        optionDesc='Desc for Option 2\nText',
        reasons='Option 1 is silly'
    )

    return Question(
        questionID=1,
        scheme=[yes_no_scheme, score_scheme],
        questionWording='Question Wording',
        findWinner=['yesNo', 'score', 'random'],
        options=[option_1, option_2]
    )


def test_oauth_config(oauth_config):
    """Tests multiple data types, including datetime"""

    jso = oauth_config.to_json()
    assert 'server' in jso
    assert '["a", "b"]' in jso
    dc_back = OAuthConfig.from_json(jso)
    assert dc_back == oauth_config


def test_yes_no_scheme(yes_no_scheme):
    """Tests enum value handling and dataclass inheritance"""
    jso = yes_no_scheme.to_json()
    assert 'yesNo' in jso
    assert 'quorum' in jso
    assert '3' in jso

    dc_back = YesNoScheme.from_json(jso)
    assert dc_back == yes_no_scheme


def test_election_config(oauth_config, question):
    questions = [question]
    config = ElectionConfig(
        electionId=str(uuid4()),
        electionTitle='test',
        auth=Auth.OAUTH,
        authData=oauth_config,
        tally=Tally.CONFIGURABLE,
        questions=questions
    )
    jso = config.to_json()
    dc_back = ElectionConfig.from_json(jso)
    # XXX: scheme is polymorphic and deserializing JSON doesn't return the original type.
    # XXX: Therefore, we expect it to differ.
    config.questions[0].scheme = None
    dc_back.questions[0].scheme = None
    assert dc_back == config
