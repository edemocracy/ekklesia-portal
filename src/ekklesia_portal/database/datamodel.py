#!/usr/bin/env python
# coding: utf-8
#
# Portal models
#
# Copyright (C) 2016-2017 by Thomas T. <ekklesia@heterarchy.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# For more details see the file COPYING.

import enum
from sqlalchemy import (
    select,
    Column,
    Integer,
    Boolean,
    Text,
    String,
    Date,
    DateTime,
    Time,
    ForeignKey,
    Sequence,
    JSON,
    func,
    Enum
)
from sqlalchemy.orm import relationship, backref, object_session
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_searchable import make_searchable
from sqlalchemy_utils.types import TSVectorType

from ekklesia_portal.database import Base
from ekklesia_portal.enums import EkklesiaUserType, PropositionStatus, SupporterStatus
from ekklesia_portal.helper.utils import cached_property


make_searchable(Base.metadata, options={'regconfig': 'pg_catalog.german'})


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, Sequence('id_seq', optional=True), primary_key=True)
    name = Column(String(64), unique=True, nullable=False)
    permissions = Column(Integer, server_default='0')
    members = association_proxy('group_members', 'member')  # <-GroupMember-> User


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('id_seq', optional=True), primary_key=True)
    name = Column(String(64), unique=True, nullable=False)
    email = Column(String(254), unique=True)  # optional, for notifications, otherwise use user/mails/
    auth_type = Column(String(8), nullable=False, server_default='system')  # deleted,system,virtual,oauth(has UserProfile)
    joined = Column(DateTime, nullable=False, server_default=func.now())
    active = Column(Boolean, nullable=False, server_default='true')
    last_active = Column(DateTime, nullable=False, server_default=func.now())  # last relevant activity (to be considered active member §2.2)
    # actions: submit/support proposition, voting, or explicit, deactivate after 2 periods
    profile = relationship("UserProfile", uselist=False, back_populates="user")
    groups = association_proxy('member_groups', 'group')  # <-GroupMember-> Group
    # from user/membership/ all_nested_groups
    departments = association_proxy('member_departments', 'department')  # <-DepartmentMember-> Department
    areas = association_proxy('member_areas', 'area')  # <-AreaMember-> SubjectArea
    supports = association_proxy('member_propositions', 'proposition')  # <-Supporter-> Proposition
    arguments = relationship("Argument", back_populates="author")
    secret_voters = association_proxy('member_secretvoters', 'secretvoter')  # <-SecretVoter-> Ballot
    urns = association_proxy('member_urns', 'urn')  # <-UrnSupporter-> Urn
    postal_votes = association_proxy('member_postal', 'voting')  # <-PostalVote-> VotingPhase


class UserPassword(Base):
    __tablename__ = 'userpassword'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    user = relationship("User", backref=backref("password", uselist=False))
    hashed_password = Column(Text)


class UserProfile(Base):
    __tablename__ = 'userprofiles'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    user = relationship("User", back_populates="profile")
    auid = Column(String(36), unique=True)  # from user/auid/
    # possibly cached variables from IDserver
    user_type = Column(Enum(EkklesiaUserType), nullable=False)  # from user/membership/
    verified = Column(Boolean)
    profile = Column(Text)  # from user/profile/
    public_id = Column(Text)  # from user/profile/
    avatar = Column(Text)  # from user/profile/
    # possible extensions
    privacy = Column(String(10))  # default,anonymous,trusted,members,users,public


class OAuthToken(Base):
    __tablename__ = 'oauth_token'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    user = relationship("User", backref=backref("oauth_token", uselist=False))
    token = Column(JSON)
    provider = Column(Text)
    created_at = Column(DateTime, nullable=False, server_default=func.now())


class GroupMember(Base):
    __tablename__ = 'groupmembers'

    group_id = Column(Integer, ForeignKey('groups.id'), primary_key=True)
    member_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    group = relationship("Group", backref=backref("group_members", cascade="all, delete-orphan"))
    member = relationship("User", backref=backref("member_groups", cascade="all, delete-orphan"))

    def __init__(self, member=None, group=None):
        self.member = member
        self.group = group


class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, Sequence('id_seq', optional=True), primary_key=True)
    name = Column(String(64), unique=True, nullable=False)
    description = Column(Text)
    members = association_proxy('department_members', 'member')  # <-DepartmentMember-> User
    areas = relationship("SubjectArea", back_populates="department")
    # parent, depth?
    configuration = Column(Text)  # JSON
    """
    durations as INT+ENUM(days,weeks,months,periods)? quorum as num/denum(INT)?

     expireActivity DURATION # inactive after periods (2) §2.2 (active by which actions?)
     memberTolerance DURATION # non-member tolerance duration (3 months) §3.6
     targetDayDistance DURATION # min. duration between target days (4 weeks, NRW 8 weeks) §4.1
     phaseDeadline DURATION # deadline for sending date announcement before target date (6 weeks) §4.1
     reorderPropositions BOOL # reorder propositions (false, NRW: true) §4.2
     votingsPerPeriod INT # recommended votings per period (20) §5.2
     assignementDeadline DURATION # deadline for secret/assignments before target date (5 weeks) §4.2
     qualificationDeadline DURATION # deadline for first proposition before target date (7 weeks) §4.2
     conflictingDeadline DURATION # deadline for conflicting proposition before target date (5 weeks) §4.2
     invitationDeadline DURATION # deadline for sending voting invitations before target date (4 weeks) §4.3
     postalVoteDeadline DURATION # deadline for secret vote request before voting starts (1 weeks) §4.4
     anonymousVoting BOOL # (false,NRW true) §5.1
     urnVoting BOOL # (true) §5.1
     postalVoteDeadline DURATION # deadline for postal vote request before target date (1 week) $5.4
     registrationDeadline DURATION # deadline for vote registration before voting starts (3 days) $5.6
     urnResponsible INT # minimum responsible members for urn (2) §5b.2
     urnVoters INT  # minimum urn voters (Bund/NRW 10, BY/HE 5) §5b.2
     urnDeadline DURATION # deadline for urn proposition before target day (4 weeks) §5b.2, §4.3
     urnAcceptance DURATION # notification deadline for urn acceptance (3 weeks) §5b.2
     urnFinalAssignments DURATION # notification deadline for final urn assignments before target day (3 days) §5b.3
     urnAssignments DURATION # notification deadline for urn assignment before target day (2 weeks) §5b.4
     urnReassignment DURATION # deadline for urn reassignment before target day (1 week) §5b.4
     urnClosing TIME # urn closing time (18:00) §5b.5
     urnDuration TIME # urn minimum duration (2 hours) §5b.5
     urnMergeLimit INT # urn merge limit (10) §5b.6
     extendedDiscussion BOOL #  (false) whether all argument relations are supported, otherwised only pro/contra and 1 level of refusal
    """


class DepartmentMember(Base):
    __tablename__ = 'departmentmembers'
    department_id = Column(Integer, ForeignKey('departments.id'), primary_key=True)
    department = relationship("Department", backref=backref("department_members", cascade="all, delete-orphan"))
    member_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    member = relationship("User", backref=backref("member_departments", cascade="all, delete-orphan"))
    is_admin = Column(Boolean, nullable=False, server_default='false')

    def __init__(self, department=None, member=None, is_admin=None):
        self.department = department
        self.member = member
        self.is_admin = is_admin


class SubjectArea(Base):  # Themenbereich §2.3+4
    __tablename__ = 'subjectareas'
    id = Column(Integer, Sequence('id_seq', optional=True), primary_key=True)
    name = Column(String(64), nullable=False)
    description = Column(Text)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)
    department = relationship("Department", back_populates="areas")
    ballots = relationship("Ballot", back_populates="area")
    # Themenbereichsteilnehmer
    # can only be removed if not proposition in this area supported §2.3
    members = association_proxy('area_members', 'member')  # <-AreaMember-> User


class AreaMember(Base):
    __tablename__ = 'areamembers'
    area_id = Column(Integer, ForeignKey('subjectareas.id'), primary_key=True)
    area = relationship("SubjectArea", backref=backref("area_members", cascade="all, delete-orphan"))
    member_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    member = relationship("User", backref=backref("member_areas", cascade="all, delete-orphan"))

    def __init__(self, area=None, member=None):
        self.area = area
        self.member = member


class Policy(Base):  # Regelwerk
    __tablename__ = 'policies'
    id = Column(Integer, Sequence('id_seq', optional=True), primary_key=True)
    name = Column(String(64), unique=True, nullable=False)
    proposition_types = relationship("PropositionType", back_populates="policy")
    configuration = Column(Text)  # JSON
    """
    configuration values also see department
         submissionQuorum INT # (5) §3.3
         retractionDuration DURATION # (1 week) §3.4
         takeoverSupporters INT # (5) §3.4
         supportExpiration DURATION # support expiration time (12 weeks) §3.5
         qualificationQuorum FRACTION # (10%) §3.5
         qualificationElection INT # absolute qualification quorum (20) §3.9
         areaMinimum INT # min. subject area members (500, BY/HE/NRW 250) §3.6
         secretQuorum FRACTION # secret vote quorum (5%) §3.5
         secretMinimum INT # min. secret vote members (50, BY/HE/NRW 25) §3.7
         propositionExpiration DURATION # (6 months) §3.8
         votingDuration DURATION # (2 weeks) §4.5
         certificateDuration DURATION # for secret ballot before voting starts (NRW 2 weeks) §4.5
         minCertificates INT # minimum valid certs for secret ballot(NRW 2) §5d.3+5
         topicLockDuration DURATION # (12 month) §4.8
         majority FRACTION # (1/2) $5d.1
         votingSystem ENUM # (range+approve voting) $5d.3
         rangeMax INT # (9) $5d.3
         rangeSmallMax INT # (3) $5d.3
         rangeSmallOptions INT # (5) $5d.3
         alwayssecret BOOL # §3.8
         election BOOL # §3.8
    """


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, Sequence('id_seq', optional=True), primary_key=True)
    name = Column(String(64), unique=True, nullable=False)
    parent_id = Column(Integer, ForeignKey('tags.id'))  # optional
    children = relationship("Tag", backref=backref('parent', remote_side=[id]))
    mut_exclusive = Column(Boolean, nullable=False, server_default='false')  # whether all children are mutually exclusive
    propositions = association_proxy('tag_propositions', 'proposition')  # <-PropositionTag-> Proposition


class PropositionType(Base):  # Antragsart
    __tablename__ = 'propositiontypes'
    id = Column(Integer, Sequence('id_seq', optional=True), primary_key=True)
    name = Column(String(64), unique=True, nullable=False)
    policy_id = Column(Integer, ForeignKey('policies.id'), nullable=False)
    policy = relationship("Policy", back_populates="proposition_types")
    ballots = relationship("Ballot", back_populates="proposition_type")


class Ballot(Base):  # conflicting qualified propositions
    __tablename__ = 'ballots'
    id = Column(Integer, Sequence('id_seq', optional=True), primary_key=True)
    name = Column(String(64), unique=True, nullable=False)
    # <- propositions Proposition[]
    status = Column(String(8), nullable=False)  # submitted?, qualified, locked, obsolete # §4.8 §5.2
    election = Column(Integer, nullable=False, server_default='0')  # 0=no election, otherwise nr of positions, §5d.4+5
    # §3.8, one proposition is for qualification of election itself
    type = Column(String(8), nullable=False)  # online, urn, assembly, board
    proposition_type_id = Column(Integer, ForeignKey('propositiontypes.id'))
    proposition_type = relationship("PropositionType", back_populates="ballots")

    area_id = Column(Integer, ForeignKey('subjectareas.id'))
    area = relationship("SubjectArea", back_populates="ballots")  # contains department

    # optional, if assigned, set proposition to planned
    voting_id = Column(Integer, ForeignKey('votingphases.id'))
    voting = relationship("VotingPhase", back_populates="ballots")

    secret_voters = association_proxy('ballot_members', 'member')  # <-SecretVoter-> User

    propositions = relationship("Proposition", back_populates="ballot")
    # <-result   VotingResult # optional
    result = relationship("VotingResult", uselist=False, back_populates="ballot")
    # <-  propositions Proposition[]
    # requirements for assignment:
    #  deadline for first and conflicting proposition before target date §4.2
    #  later conflicting proposition are assigned to a new independent ballot


class SecretVoter(Base):  # §3.7, §4.4
    __tablename__ = 'secretvoters'
    member_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    member = relationship("User", backref=backref("member_ballots", cascade="all, delete-orphan"))
    ballot_id = Column(Integer, ForeignKey('ballots.id'), primary_key=True)
    ballot = relationship("Ballot", backref=backref("ballot_members", cascade="all, delete-orphan"))

    status = Column(String(10), nullable=False)  # active,expired,retracted
    last_change = Column(Date, nullable=False)  # time of requested/retracted
    # can only be requested before deadline before voting starts §4.4
    # qualification §4.4 (immediate check): for count active members (minimum number §3.7),
    #  calculate quorum, if supporters >= quorum, set ballot to secret


class VotingPhase(Base):  # Abstimmungsperiode
    __tablename__ = 'votingphases'
    id = Column(Integer, Sequence('id_seq', optional=True), primary_key=True)
    target = Column(Date, nullable=False)  # constrained by §4.1
    secret = Column(Boolean, nullable=False, server_default='false')  # whether any secret votes will take place (decision deadline §4.2)
    ballots = relationship("Ballot", back_populates="voting")
    # <- urns    Urn[]
    urns = relationship("Urn", back_populates="voting")
    postal_votes = association_proxy('voting_postal', 'member')  # <-PostalVote-> User
    # send announcement before deadline §4.1
    # send voting invitation before deadline §4.3
    # deadline for vote registration before voting starts $5.6
    # shall not assign more than recommended votings per period §5.2
    # ask submitters for veto for move to other phase §5.3


class VotingResult(Base):  # §4.6, move to ballot?
    __tablename__ = 'votingresults'
    id = Column(Integer, Sequence('id_seq', optional=True), primary_key=True)
    data = Column(Text)  # JSON or ID share reference or compressed result?
    ballot_id = Column(Integer, ForeignKey('ballots.id'))
    ballot = relationship("Ballot", back_populates="result")


class Proposition(Base):
    __tablename__ = 'propositions'
    id = Column(Integer, Sequence('id_seq', optional=True), primary_key=True)
    title = Column(Text, nullable=False)
    content = Column(Text, nullable=False)  # modifies: generate diff to original dynamically
    abstract = Column(Text, nullable=False, server_default='')
    motivation = Column(Text, nullable=False, server_default='')
    submitted = Column(Date)  # optional, §3.1, for order of voting §5.3, date of change if original (§3.4)
    qualified = Column(Date)  # optional, when qualified
    status = Column(Enum(PropositionStatus), nullable=False, server_default='DRAFT')
    ballot_id = Column(Integer, ForeignKey('ballots.id'))
    ballot = relationship("Ballot", uselist=False, back_populates="propositions")  # contains area (department), propositiontype
    supporters = association_proxy('propositions_member', 'member')  # <-Supporter-> User
    # in state draft only submitters may become supporters §3.3
    tags = association_proxy('proposition_tags', 'tag')  # <-PropositionTag-> Tag

    modifies_id = Column(Integer, ForeignKey('propositions.id'))  # optional, only one level allowed
    derivations = relationship("Proposition", foreign_keys=[modifies_id], backref=backref('modifies', remote_side=[id]))

    replaces_id = Column(Integer, ForeignKey('propositions.id'))  # optional
    replacements = relationship("Proposition", foreign_keys=[replaces_id], backref=backref('replaces', remote_side=[id]))

    discussion_url = Column(Text)

    created_at = Column(DateTime, nullable=False, server_default=func.now())

    search_vector = Column(TSVectorType('title', 'abstract', 'content', 'motivation',
                                        weights={'title': 'A', 'abstract': 'B', 'content': 'C', 'motivation': 'D'}))

    def support_by_user(self, user):
        for s in self.propositions_member:
            if s.member_id == user.id and s.status == SupporterStatus.ACTIVE:
                return s

    @hybrid_property
    def active_supporter_count(self):
        return len([s for s in self.propositions_member if s.status == SupporterStatus.ACTIVE])

    @active_supporter_count.expression
    def active_supporter_count(cls):
        return select([func.count()]).where(Supporter.proposition_id == cls.id).where(Supporter.status == SupporterStatus.ACTIVE)

    """
   submission data: content, submitters, conflicts
   perform daily checks
   change only if submitted §3.4:
    1. create copy as draft until all submitters agree (set parent)
    2. copy supporters to new proposition and replace original in its conflicts
       for original: set status to changing and original submitters to retracted (takeover submitters= active)
    3a. if takeover within timelimit, submit new version as new conflicting proposition and remove old supporters, original status=submitted
    3b. otherwise set original to abandoned
   retraction: when all retracted and timelimit passed, set to status abandoned, remove from conflicts
   qualification §3.5 (immediate check): for each area count members (minimum number §3.6), calculate quorum,
   if supporters >= quorum, set to state qualified
   expiration: for submitted proposition, if supporter > expiration time, set to expired
     if proposition in submitted state for proposition expiration time §3.8, set to abandoned, expire supporters?
     if vote on Parteitag, set to finished with results §3.8
   elections: first normal proposition for election itself, then candidates in ballot §3.9
    """


class PropositionTag(Base):
    __tablename__ = 'propositiontags'
    proposition_id = Column(Integer, ForeignKey('propositions.id'), primary_key=True)
    proposition = relationship("Proposition", backref=backref("proposition_tags", cascade="all, delete-orphan"))
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)
    tag = relationship("Tag", backref=backref("tag_propositions", cascade="all, delete-orphan"))

    def __init__(self, tag=None, proposition=None):
        self.tag = tag
        self.proposition = proposition


class Supporter(Base):  # §3.5
    __tablename__ = 'supporters'
    member_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    member = relationship("User", backref=backref("member_propositions", cascade="all, delete-orphan"))
    proposition_id = Column(Integer, ForeignKey('propositions.id'), primary_key=True)
    proposition = relationship("Proposition", backref=backref("propositions_member", cascade="all, delete-orphan"))
    submitter = Column(Boolean, nullable=False, server_default='false')  # submitter or regular
    status = Column(Enum(SupporterStatus), nullable=False, server_default='ACTIVE')
    last_change = Column(Date, nullable=False, server_default=func.now())  # time of submitted/supported/retracted


class Argument(Base):
    __tablename__ = 'arguments'
    id = Column(Integer, Sequence('id_seq', optional=True), primary_key=True)
    title = Column(Text, nullable=False)
    abstract = Column(Text, nullable=False)
    details = Column(Text)
    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship("User", backref=backref("member_arguments", cascade="all, delete-orphan"))
    created_at = Column(DateTime, nullable=False, server_default=func.now())


class ArgumentRelation(Base):
    __tablename__ = 'argumentrelations'
    id = Column(Integer, Sequence('id_seq', optional=True), primary_key=True)
    parent_id = Column(Integer, ForeignKey('argumentrelations.id'))  # optional for inter-arguments
    children = relationship("ArgumentRelation", backref=backref('parent', remote_side=[id]))

    argument_id = Column(Integer, ForeignKey('arguments.id'))
    argument = relationship("Argument", backref=backref("argument_relations", cascade="all, delete-orphan"))
    proposition_id = Column(Integer, ForeignKey('propositions.id'))  # also show parent proposition arguments if still valid?
    proposition = relationship("Proposition", backref=backref("proposition_arguments", cascade="all, delete-orphan"))
    argument_type = Column(String(8), nullable=False)  # pro/extends,contra/refutes,question,answer
    # if not extendedDiscussion: only pro/contra/refutes

    def user_vote(self, user):
        return object_session(self).query(ArgumentVote).filter_by(relation=self, member=user).scalar()

    @cached_property
    def score(self):
        return sum(rv.weight for rv in self.relation_votes)


class ArgumentVote(Base):
    __tablename__ = 'argumentvotes'
    member_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    member = relationship("User", backref=backref("member_argumentvotes", cascade="all, delete-orphan"))
    relation_id = Column(Integer, ForeignKey('argumentrelations.id'), primary_key=True)
    relation = relationship("ArgumentRelation", backref=backref("relation_votes", cascade="all, delete-orphan"))
    weight = Column(Integer, nullable=False)  # if extendedDiscussion: --,-,0,+,++ , otherwise -1 and +1


class PostalVote(Base):  # §5.4
    __tablename__ = 'postalvotes'
    member_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    member = relationship("User", backref=backref("member_postal", cascade="all, delete-orphan"))
    voting_id = Column(Integer, ForeignKey('votingphases.id'), primary_key=True)  # option, empty=permanent
    voting = relationship("VotingPhase", backref=backref("voting_postal", cascade="all, delete-orphan"))
    # can only be requested before deadline before voting starts §5.4
    # deleted when member becomes inactive
    # must not be urn supporter


class Urn(Base):
    __tablename__ = 'urns'
    id = Column(Integer, Sequence('id_seq', optional=True), primary_key=True)
    voting_id = Column(Integer, ForeignKey('votingphases.id'), nullable=False)
    voting = relationship("VotingPhase", back_populates="urns")
    accepted = Column(Boolean, nullable=False, server_default='false')
    location = Column(Text, nullable=False)
    description = Column(Text)
    opening = Column(Time)  # §5b.5
    supporters = association_proxy('urn_members', 'member')  # <-UrnSupporter-> User
    # see deadlines and requirements in config


class UrnSupporter(Base):  # §5b.2
    __tablename__ = 'urnsupporters'
    member_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    member = relationship("User", backref=backref("member_urns", cascade="all, delete-orphan"))
    urn_id = Column(Integer, ForeignKey('urns.id'), primary_key=True)
    urn = relationship("Urn", backref=backref("urn_members", cascade="all, delete-orphan"))

    type = Column(String(12), nullable=False)  # responsible, request, voter # §5b.2+4
    voted = Column(Boolean, nullable=False, server_default='false')  # §5b.6
    # urn merge if below min. no of voters §5b.6
