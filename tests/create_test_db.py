if __name__ == "__main__":
    from datetime import timedelta
    import logging
    import sqlalchemy.orm
    import mimesis
    from ekklesia_portal.lib.password import password_context
    logging.basicConfig(level=logging.INFO)
    import transaction
    from ekklesia_portal.app import make_wsgi_app

    app = make_wsgi_app("./config.yml")

    logg = logging.getLogger(__name__)

    from ekklesia_portal.database import db_metadata, Session
    from ekklesia_portal.database.datamodel import *

    logg.info("using db url %s", app.settings.database.uri)

    sqlalchemy.orm.configure_mappers()

    db_metadata.drop_all()
    db_metadata.create_all()

    s = Session()

    gen_de = mimesis.Generic('de')

    department_pps = Department(name='PPS')
    department_zs = Department(name='Zentralschweiz')

    subject_area_pps_in = SubjectArea(name='Innerparteiliches', department=department_pps)
    subject_area_zs_in = SubjectArea(name='Innerparteiliches', department=department_zs)
    subject_area_pps_pol = SubjectArea(name='Politik', department=department_pps)

    ug1 = Group(name="Deppengruppe")

    u1 = User(name="testuser", auth_type="system")
    u1.password = UserPassword(hashed_password=password_context.hash("test", scheme="plaintext"))
    u2_profile = UserProfile(auid='auid_egon', user_type=EkklesiaUserType.PLAIN_MEMBER, verified=True, avatar='xxx', profile='ich halt')
    u2_oauth_token = OAuthToken(provider='ekklesia', token={})
    u2 = User(name="egon", auth_type="oauth", profile=u2_profile, oauth_token=u2_oauth_token)
    ug1.members.extend([u1, u2])
    s.add(DepartmentMember(department=department_pps, member=u1, is_admin=True))
    u2.departments.extend([department_pps, department_zs])
    u1.areas.extend([subject_area_pps_in])
    u2.areas.extend([subject_area_pps_in, subject_area_pps_pol, subject_area_zs_in])

    voting_phase_type_pv = VotingPhaseType(name='Piratenversammlung', voting_type=VotingType.ASSEMBLY,
                                           abbreviation='PV', secret_voting_possible=True)
    voting_phase_type_ur = VotingPhaseType(name='Online-Urabstimmung', voting_type=VotingType.ONLINE,
                                           abbreviation='UR', secret_voting_possible=False)

    voting_phase_pps_online = VotingPhase(phase_type=voting_phase_type_ur, target='2018-11-11', status=VotingStatus.SCHEDULED)
    voting_phase_pps_pv = VotingPhase(phase_type=voting_phase_type_pv,
                                      secret=True,
                                      title='Piratenversammlung 2018.2',
                                      name='pv182',
                                      description='eine **Piratenversammlung** in der Schweiz')

    department_pps.voting_phases.extend([voting_phase_pps_online, voting_phase_pps_pv])

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
        submitter_minimum=5,
        voting_duration=14,
        voting_system=VotingSystem.RANGE_APPROVAL)

    s.add(policy_default)

    ptype_pol = PropositionType(name='Politische Position', description=gen_de.text.text(quantity=3), policy=policy_default)
    s.add(ptype_pol)

    t1 = Tag(name="Tag1")
    t2 = Tag(name="Tag2")
    t3 = Tag(name="Täääg3")

    b1 = Ballot(area=subject_area_pps_in)
    s.add(b1)
    q1 = Proposition(title="Ein Titel", content=gen_de.text.text(quantity=40))

    q1_counter = Proposition(title="Gegenantrag zu Q1", content="will was anderes", replaces=q1)

    q1_counter_2 = Proposition(title="Noch ein Gegenantrag zu Q1 mit Volltextsuche",
                               content="will was ganz anderes, ich will Volltextsuche", replaces=q1)
    q1_change = Proposition(title="Änderungsantrag zu Q1", content="will was ändern", modifies=q1)
    b1.propositions.extend([q1, q1_counter, q1_counter_2, q1_change])

    arg1 = Argument(author=u1,
                    title="Ein Pro-Argument",
                    abstract=gen_de.text.text(quantity=2)[:140],
                    details=gen_de.text.text(quantity=10))
    arg2 = Argument(author=u2, title="Ein zweites Pro-Argument", abstract="dafür!!!")
    arg3 = Argument(author=u1, title="Ein Contra-Argument", abstract="dagegen!!!", details="aus Gründen")

    arg1_rel = ArgumentRelation(proposition=q1, argument=arg1, argument_type=ArgumentType.PRO)
    arg2_rel = ArgumentRelation(proposition=q1, argument=arg2, argument_type=ArgumentType.PRO)
    arg3_rel = ArgumentRelation(proposition=q1, argument=arg3, argument_type=ArgumentType.CONTRA)

    q1.proposition_arguments.extend([arg1_rel, arg2_rel, arg3_rel])
    q1.tags.extend([t1, t2])
    s.add(q1)

    b2 = Ballot(area=subject_area_pps_pol)
    s.add(b2)
    q2 = Proposition(title="Noch Ein Titel", content=gen_de.text.text(quantity=20))
    q2.tags.append(t3)
    b2.propositions.append(q2)

    qv1 = Supporter(member=u1, proposition=q1, submitter=True)
    s.add(qv1)
    qv2 = Supporter(member=u2, proposition=q1_counter, submitter=True)
    s.add(qv2)
    qv3 = Supporter(member=u1, proposition=q2)
    s.add(qv3)
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

    logg.info("commited")
