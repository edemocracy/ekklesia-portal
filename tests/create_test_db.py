import argparse
import logging
from datetime import datetime
import os

from alembic.config import Config
from alembic import command
import mimesis
import sqlalchemy.orm
import transaction
from ekklesia_common.ekklesia_auth import OAuthToken

from ekklesia_portal.app import make_wsgi_app
from ekklesia_portal.enums import ArgumentType, Majority, PropositionStatus, SupporterStatus, VotingStatus, VotingSystem, VotingType
from ekklesia_portal.lib.password import password_context

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser("Ekklesia Portal create_test_db.py")
parser.add_argument("-c", "--config-file", help=f"path to config file in YAML / JSON format")

DOCUMENT_WP = '''# Wahlprogramm

## Section 1 {data-section="1"}

### Section 1.1 {data-section="1.1"}

Text Section 1.1
'''

PUSH_DRAFT_EXTERNAL_TEMPLATE = '''
Dieser Antragsentwurf wurde automatisch erstellt durch das Antragsportal

{draft_link}

## Vorbemerkungen / Bearbeitungshinweise

(nicht Teil des Antrags)

{editing_remarks}

## Zusammenfassung

{abstract}

## Antragstext

{content}

## Begründung

{motivation}
'''

PUSH_DRAFT_PORTAL_TEMPLATE = '''
Der Antragsentwurf wird hier weiterentwickelt:

{topic_url}

Verbesserungsvorschläge und Verständnisfragen bitte dort einbringen.
'''

DOCUMENT_PROPOSE_CHANGE_EXPLANATION_DE = '''
Stelle einen Wahlprogrammantrag, um dieses Programm zu ändern.
Du kannst eine Änderung an einem Abschnitt vorschlagen, indem du auf dessen Überschrift klickst.
Auf der folgenden Seite kannst du den Text bearbeiten und weitere Informationen zu deinen Antragsentwurf ergänzen.
'''

NEW_DRAFT_EXPLANATION_DE = '''
Nach dem Abschicken wird dein Antragsentwurf automatisch im Forum in der Kategorie Antragsentwicklung eingestellt.
Der Text des Antrags kann dort von allen angemeldeten Benutzern bearbeitet werden wie in einem Wiki.
Du kannst die Bearbeitung sperren lassen. Wende dich dazu an die Antragskommission.
'''


if __name__ == "__main__":

    logg = logging.getLogger(__name__)

    args = parser.parse_args()

    app = make_wsgi_app(args.config_file)

    # Needed for Alembic env.py
    if args.config_file:
        os.environ['EKKLESIA_PORTAL_CONFIG'] = args.config_file
    if 'EKKLESIA_PORTAL_CONFIG' not in os.environ:
        os.environ['EKKLESIA_PORTAL_CONFIG'] = "config.yml"

    from ekklesia_common.database import db_metadata, Session
    # local import because we have to set up the database stuff before that
    from ekklesia_portal.datamodel import (
        Argument, ArgumentRelation, ArgumentVote, Ballot, CustomizableText, Department, DepartmentMember, Document,
        Group, Policy, Proposition, PropositionType, SubjectArea, Supporter, Tag, User, UserPassword, UserProfile,
        VotingPhase, VotingPhaseType
    )

    print(f"using config file {args.config_file}")
    print(f"using db url {app.settings.database.uri}")

    engine = sqlalchemy.create_engine(app.settings.database.uri)
    connection = engine.connect()
    connection.execute("select")

    sqlalchemy.orm.configure_mappers()

    print(80 * "=")
    input("press Enter to drop and create the database...")

    db_metadata.drop_all()
    connection.execute("DROP TABLE IF EXISTS alembic_version")
    db_metadata.create_all()

    s = Session()

    gen_de = mimesis.Generic('de')

    s.add(CustomizableText(lang='de', name='push_draft_external_template', text=PUSH_DRAFT_EXTERNAL_TEMPLATE))
    s.add(CustomizableText(lang='de', name='push_draft_portal_template', text=PUSH_DRAFT_PORTAL_TEMPLATE))
    s.add(
        CustomizableText(
            lang='de', name='document_propose_change_explanation', text=DOCUMENT_PROPOSE_CHANGE_EXPLANATION_DE
        )
    )
    s.add(CustomizableText(lang='de', name='new_draft_explanation', text=NEW_DRAFT_EXPLANATION_DE))

    department_pps = Department(name='Piratenpartei Schweiz')
    department_zs = Department(name='Zentralschweiz')
    department_ppd = Department(name='Piratenpartei Deutschland')

    department_ppd.exporter_settings = {"exporter_name": "testdiscourse", "exporter_description": "Ein Test-Discourse"}

    department_by = Department(name='Landesverband Bayern')
    department_opf = Department(name='Bezirksverband Oberpfalz')
    s.add(department_by)
    s.add(department_opf)

    subject_area_pps_in = SubjectArea(name='Innerparteiliches', department=department_pps)
    subject_area_zs_in = SubjectArea(name='Innerparteiliches', department=department_zs)
    subject_area_pps_pol = SubjectArea(name='Politik', department=department_pps)
    subject_area_ppd_allg = SubjectArea(name='Allgemein', department=department_ppd)

    ug1 = Group(name="Deppengruppe")
    admin_group = Group(name="Göttliche Admins", is_admin_group=True)
    s.add(admin_group)

    u1 = User(name="testuser", auth_type="system")
    admin = User(name="testadmin", auth_type="system")
    admin.password = UserPassword(hashed_password=password_context.hash("admin", scheme="plaintext"))
    admin_group.members.append(admin)

    u1.password = UserPassword(hashed_password=password_context.hash("test", scheme="plaintext"))
    u2_profile = UserProfile(sub='sub_egon', eligible=True, verified=True, profile='ich halt')
    u2_oauth_token = OAuthToken(provider='ekklesia', token={})
    u2 = User(name="egon", auth_type="oauth", profile=u2_profile, oauth_token=u2_oauth_token)
    u3_profile = UserProfile(sub='sub_olaf', eligible=False, verified=True, profile='## Markdown\n\nText')
    u3_oauth_token = OAuthToken(provider='ekklesia', token={})
    u3 = User(name="olaf", auth_type="oauth", profile=u3_profile, oauth_token=u3_oauth_token)
    ug1.members.extend([u1, u2, u3])
    s.add(DepartmentMember(department=department_ppd, member=u1))
    s.add(DepartmentMember(department=department_pps, member=u1))
    s.add(DepartmentMember(department=department_ppd, member=u3))
    u2.departments.extend([department_zs])
    u1.areas.extend([subject_area_ppd_allg, subject_area_pps_in])
    u2.areas.extend([subject_area_zs_in])
    u3.areas.extend([subject_area_ppd_allg])

    voting_phase_type_ur = VotingPhaseType(
        name='Online-Urabstimmung', voting_type=VotingType.ONLINE, abbreviation='UR', secret_voting_possible=False
    )
    voting_phase_type_bpt = VotingPhaseType(
        name='Bundesparteitag', voting_type=VotingType.ASSEMBLY, abbreviation='BPT', secret_voting_possible=True
    )

    voting_phase_ppd_bpt_scheduled = VotingPhase(
        phase_type=voting_phase_type_bpt,
        target='2020-11-11',
        status=VotingStatus.SCHEDULED,
        secret=True,
        title='BPT 2020.1',
        name='bpt201',
        description='Der nächste Parteitag irgendwo'
    )

    department_ppd.voting_phases.extend([voting_phase_ppd_bpt_scheduled])

    voting_phase_zs_ur = VotingPhase(
        phase_type=voting_phase_type_ur,
        status=VotingStatus.PREPARING,
        title='Urabstimmung 2019+',
        name='ur19+',
        description='eine **Urabstimmung** in Zentalschweiz'
    )

    department_zs.voting_phases.extend([voting_phase_zs_ur])

    voting_phase_ppd_bpt = VotingPhase(
        phase_type=voting_phase_type_bpt,
        secret=True,
        title='BPT 2019.2',
        name='bpt192',
        status=VotingStatus.FINISHED,
        target="2019-11-10",
        description='Der BPT in Bad Homburg'
    )

    department_ppd.voting_phases.extend([voting_phase_ppd_bpt])

    policy_default = Policy(
        description=gen_de.text.text(quantity=3),
        name='default',
        majority=Majority.SIMPLE,
        proposition_expiration=180,
        qualification_quorum=0.1,
        qualification_minimum=50,
        range_max=9,
        range_small_max=3,
        range_small_options=5,
        secret_minimum=20,
        secret_quorum=0.05,
        submitter_minimum=2,
        voting_duration=14,
        voting_system=VotingSystem.RANGE_APPROVAL
    )

    s.add(policy_default)

    ptype_pol = PropositionType(
        name='Positionspapier', abbreviation='PP', description=gen_de.text.text(quantity=3), policy=policy_default
    )
    s.add(ptype_pol)

    ptype_wp = PropositionType(
        name='Wahlprogrammantrag', abbreviation='WP', description=gen_de.text.text(quantity=3), policy=policy_default
    )
    s.add(ptype_wp)

    doc_wp = Document(
        name='Wahlprogramm',
        lang='de',
        area=subject_area_ppd_allg,
        description='Ein Wahlprogramm',
        proposition_type=ptype_wp,
        text=DOCUMENT_WP
    )
    s.add(doc_wp)

    t1 = Tag(name="Tag1")
    t2 = Tag(name="Tag2")
    t3 = Tag(name="Täääg3")

    b1 = Ballot(area=subject_area_pps_in, voting=voting_phase_ppd_bpt_scheduled, name="PP001/2/3/4", proposition_type=ptype_pol)
    s.add(b1)
    q1 = Proposition(
        title="Ein Titel",
        content=gen_de.text.text(quantity=40),
        voting_identifier="PP001",
        external_discussion_url="http://example.com",
        created_at=datetime.fromisoformat('2020-01-01'),
        submitted_at=datetime.fromisoformat('2020-01-05'),
        qualified_at=datetime.fromisoformat('2020-01-08'),
        status=PropositionStatus.SCHEDULED
    )

    q1_counter = Proposition(
        title="Gegenantrag zu PP001",
        content="will was anderes",
        voting_identifier="PP002",
        replaces=q1,
        created_at=datetime.fromisoformat('2020-01-02'),
        submitted_at=datetime.fromisoformat('2020-01-07'),
        qualified_at=datetime.fromisoformat('2020-01-10'),
        status=PropositionStatus.SCHEDULED
    )

    q1_counter_2 = Proposition(
        title="Noch ein Gegenantrag zu PP001 mit Volltextsuche",
        content="will was ganz anderes, ich will Volltextsuche",
        voting_identifier="PP003",
        replaces=q1,
        created_at=datetime.fromisoformat('2020-01-03'),
        submitted_at=datetime.fromisoformat('2020-01-09'),
        qualified_at=datetime.fromisoformat('2020-01-24'),
        status=PropositionStatus.SCHEDULED
    )
    q1_change = Proposition(
        title="Änderungsantrag zu PP001",
        content="will was ändern",
        voting_identifier="PP004",
        modifies=q1,
        created_at=datetime.fromisoformat('2020-01-06'),
        submitted_at=datetime.fromisoformat('2020-01-06'),
        qualified_at=datetime.fromisoformat('2020-01-11'),
        status=PropositionStatus.SCHEDULED
    )
    b1.propositions.extend([q1, q1_counter, q1_counter_2, q1_change])
    q6 = Proposition(
        title="Fallengelassener Antrag",
        content="Einfach so fallengelassen...",
        external_discussion_url="http://example.com",
        created_at=datetime.fromisoformat('2020-01-01'),
        status=PropositionStatus.ABANDONED
    )
    q6.tags.append(t3)
    b6 = Ballot(area=subject_area_pps_in, proposition_type=ptype_pol)
    s.add(b6)
    b6.propositions.append(q6)
    q7 = Proposition(
        title="Sich ändernder Antrag",
        content="Einfach so ändernd...",
        external_discussion_url="http://example.com",
        created_at=datetime.fromisoformat('2020-01-01'),
        status=PropositionStatus.CHANGING
    )
    q7.tags.append(t3)
    b7 = Ballot(area=subject_area_pps_in, proposition_type=ptype_pol)
    s.add(b7)
    b7.propositions.append(q7)
    q8 = Proposition(
        author=u1,
        title="Entstehender Antrag",
        content="Einfach so entstehend...",
        created_at=datetime.fromisoformat('2020-01-06'),
        status=PropositionStatus.DRAFT
    )
    q8.tags.append(t3)
    b8 = Ballot(area=subject_area_pps_in, proposition_type=ptype_pol)
    s.add(b8)
    b8.propositions.append(q8)
    q9 = Proposition(
        title="Übertragener Antrag",
        content="Einfach so Übertragen...",
        external_discussion_url="http://example.com",
        created_at=datetime.fromisoformat('2020-01-06'),
        submitted_at=datetime.fromisoformat('2020-01-06'),
        status=PropositionStatus.SUBMITTED
    )
    b9 = Ballot(area=subject_area_pps_in, proposition_type=ptype_pol)
    s.add(b9)
    b9.propositions.append(q9)
    q10 = Proposition(
        title="Qualifizierter Antrag",
        content="Einfach so qualifiziert...",
        status=PropositionStatus.QUALIFIED,
        created_at=datetime.fromisoformat('2020-01-06'),
        submitted_at=datetime.fromisoformat('2020-01-06'),
        qualified_at=datetime.fromisoformat('2020-01-11'),
    )
    b10 = Ballot(area=subject_area_pps_in, proposition_type=ptype_pol)

    s.add(b10)
    b10.propositions.append(q10)
    arg1 = Argument(
        author=u1,
        title="Ein Pro-Argument",
        abstract=gen_de.text.text(quantity=2)[:140],
        details=gen_de.text.text(quantity=10)
    )
    arg2 = Argument(author=u2, title="Ein zweites Pro-Argument", abstract="dafür!!!")
    arg3 = Argument(author=u1, title="Ein Contra-Argument", abstract="dagegen!!!", details="aus Gründen")

    arg1_rel = ArgumentRelation(proposition=q1, argument=arg1, argument_type=ArgumentType.PRO)
    arg2_rel = ArgumentRelation(proposition=q1, argument=arg2, argument_type=ArgumentType.PRO)
    arg3_rel = ArgumentRelation(proposition=q1, argument=arg3, argument_type=ArgumentType.CONTRA)

    q1.proposition_arguments.extend([arg1_rel, arg2_rel, arg3_rel])
    q1.tags.extend([t1, t2])
    s.add(q1)
    q2 = Proposition(
        title="Antrag mit nicht unterstütztem Ergebnisformat",
        content=gen_de.text.text(quantity=20),
        voting_identifier="PP001",
        external_discussion_url="http://example.com",
        created_at=datetime.fromisoformat('2020-01-06'),
        submitted_at=datetime.fromisoformat('2020-01-06'),
        qualified_at=datetime.fromisoformat('2020-01-11'),
        status=PropositionStatus.FINISHED
    )
    q2.tags.append(t3)
    b2 = Ballot(area=subject_area_ppd_allg, voting=voting_phase_ppd_bpt, name="PP001", proposition_type=ptype_pol)
    s.add(b2)
    b2.propositions.append(q2)
    q3 = Proposition(
        title="Angenommener Antrag",
        content=gen_de.text.text(quantity=2),
        voting_identifier="PP005",
        external_discussion_url="http://example.com",
        created_at=datetime.fromisoformat('2020-01-06'),
        submitted_at=datetime.fromisoformat('2020-01-06'),
        qualified_at=datetime.fromisoformat('2020-01-11'),
        status=PropositionStatus.FINISHED
    )
    q3.tags.append(t3)
    b3 = Ballot(area=subject_area_ppd_allg, voting=voting_phase_ppd_bpt, name="PP005", proposition_type=ptype_pol)
    s.add(b3)
    b3.propositions.append(q3)
    q4 = Proposition(
        title="Abgelehnter Antrag",
        content="Bla",
        voting_identifier="PP006",
        external_discussion_url="http://example.com",
        created_at=datetime.fromisoformat('2020-01-06'),
        submitted_at=datetime.fromisoformat('2020-01-06'),
        qualified_at=datetime.fromisoformat('2020-01-11'),
        status=PropositionStatus.FINISHED
    )
    q4.tags.append(t3)
    b4 = Ballot(area=subject_area_ppd_allg, voting=voting_phase_ppd_bpt, name="PP006", proposition_type=ptype_pol)
    s.add(b4)
    b4.propositions.append(q4)
    q5 = Proposition(
        title="Verschobener Antrag",
        content="Blubb",
        voting_identifier="PP007",
        external_discussion_url="http://example.com",
        created_at=datetime.fromisoformat('2020-01-06'),
        submitted_at=datetime.fromisoformat('2020-01-06'),
        qualified_at=datetime.fromisoformat('2020-01-11'),
        status=PropositionStatus.FINISHED
    )
    q5.tags.append(t3)
    q5_counter = Proposition(
        title="Abgelehnter Gegenantrag zum Verschobenen Antrag PP007",
        content="Gegenantrag von PP008",
        voting_identifier="PP008",
        external_discussion_url="http://example.com",
        modifies=q5,
        created_at=datetime.fromisoformat('2020-01-06'),
        submitted_at=datetime.fromisoformat('2020-01-06'),
        qualified_at=datetime.fromisoformat('2020-01-11'),
        status=PropositionStatus.FINISHED
    )
    q5_counter.tags.append(t3)
    b5 = Ballot(area=subject_area_ppd_allg, voting=voting_phase_ppd_bpt, name="PP007/8", proposition_type=ptype_pol)
    s.add(b5)
    b5.propositions.extend([q5, q5_counter])
    b2.result = {q2.voting_identifier: {"rank": 1, "yes": 14, "no": 10, "abstention": 15, "points": 213}}
    b3.result = {q3.voting_identifier: {"state": "accepted"}}
    b4.result = {q4.voting_identifier: {"state": "rejected"}}
    b5.result = {q5.voting_identifier: {"state": "not decided"}, q5_counter.voting_identifier: {"state": "rejected"}}
    qv1 = Supporter(member=u1, proposition=q1, submitter=True)
    s.add(qv1)
    qv2 = Supporter(member=u2, proposition=q1_counter, submitter=True)
    s.add(qv2)
    qv3 = Supporter(member=u1, proposition=q2)
    s.add(qv3)
    qv6 = Supporter(member=u1, proposition=q3)
    s.add(qv6)
    qv7 = Supporter(member=u1, proposition=q4)
    s.add(qv7)
    qv8 = Supporter(member=u1, proposition=q5)
    s.add(qv8)
    qv4 = Supporter(member=u2, proposition=q1, status=SupporterStatus.RETRACTED)
    s.add(qv4)
    qv5 = Supporter(member=u2, proposition=q2, status=SupporterStatus.EXPIRED)
    s.add(qv5)

    qv1 = ArgumentVote(member=u1, relation=arg1_rel, weight=1)
    s.add(qv1)
    qv2 = ArgumentVote(member=u1, relation=arg2_rel, weight=-1)
    s.add(qv2)
    qv3 = ArgumentVote(member=u2, relation=arg1_rel, weight=-1)
    s.add(qv3)

    transaction.commit()

    logg.info("committed")

    alembic_cfg = Config("./alembic.ini")
    command.stamp(alembic_cfg, "head")
