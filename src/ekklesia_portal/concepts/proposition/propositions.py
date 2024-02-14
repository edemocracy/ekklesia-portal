from typing import Optional

import dataclasses
from dataclasses import dataclass
from eliot import log_call, Message

import sqlalchemy_searchable
from sqlalchemy import desc, func
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.functions import coalesce

from ekklesia_portal.datamodel import Ballot, Changeset, Department, Proposition, PropositionType, SubjectArea, Tag, VotingPhase, Supporter
from ekklesia_portal.enums import PropositionStatus, PropositionVisibility, PropositionRelationType, SupporterStatus


@dataclass
class Propositions:
    department: str = None
    document: int = 0
    phase: str = None
    search: str = None
    section: str = None
    sort: str = None
    status: str = None
    subject_area: str = None
    tags: str = None
    without_tags: str = None
    type: str = None
    visibility: str = None
    association_type: PropositionRelationType = None
    association_id: str = None
    include_amendments: str = None
    only_supporting: str = None
    # Initialization with numbers instead of None is necessary because otherwise the
    # query values are not actually converted to an integer on assignment
    page: Optional[int] = 1  # Ranges: x<=1 = None => First page; x>1 => Show page x
    per_page: Optional[int] = 0  # Ranges: x<0 => All on one page; x=0 = None => Use default; x>0 => Show x per page

    def __post_init__(self):
        self.parse_search_filters()

        # Force None value if argument is empty to clean up url
        self.department = self.department or None
        self.document = self.document or None
        self.phase = self.phase or None
        self.search = self.search or None
        self.section = self.section or None
        self.sort = self.sort or None
        self.tags = self.tags or None
        self.without_tags = self.without_tags or None
        self.type = self.type or None
        self.status = self.status or None
        self.include_amendments = self.include_amendments or None
        self.only_supporting = self.only_supporting or None

        self.status_values = None
        self.tag_values = None
        self.without_tag_values = None
        self.visibility_values = None

        if self.per_page is not None:
            if self.per_page == 0:
                self.per_page = None
            elif self.per_page < -1:
                self.per_page = -1

        if self.page is not None and self.page <= 1:
            self.page = None

        if self.visibility:
            try:
                self.visibility_values = [PropositionVisibility(s.strip().lower()) for s in self.visibility.split(",")]
            except (KeyError, ValueError):
                self.visibility = None

        if self.status:
            try:
                self.status_values = [PropositionStatus(s.strip().lower()) for s in self.status.split(",")]
            except (KeyError, ValueError):
                self.status = None

        if self.tags:
            self.tag_values = [t.strip().lower() for t in self.tags.split(",")]

        if self.without_tags:
            self.without_tag_values = [t.strip().lower() for t in self.without_tags.split(",")]

        # Don't display subject area filter when no department filter is given
        self.subject_area = self.subject_area if self.department and self.subject_area else None

    def parse_search_filters(self):
        if not self.search:
            return

        search = []

        key = None
        word = []
        quot_started = None
        word_done = False
        for c in self.search.strip().replace("\n", " "):
            if c in ('"', '\''):
                if quot_started == c:  # If at quoted string end
                    word_done = True
                    quot_started = None
                elif not quot_started and len(word) == 0:  # If at quoted string start
                    quot_started = c
                else:  # If quote in middle of word
                    word.append(c)

            elif c == ':':
                if quot_started:  # Colon in quoted string belongs to word
                    word.append(c)
                elif len(word) > 0:  # Only allow colons after text
                    key = ''.join(word)
                    word.clear()

            elif c == ' ':
                if quot_started:  # Whitespace in quoted string belongs to word
                    word.append(c)
                else:
                    word_done = True
            else:
                word.append(c)

            if word_done:
                word_done = False
                value = ''.join(word)
                word.clear()
                if key:
                    self.parse_search_filter(key, value)
                    key = None
                else:
                    search.append(value)  # Quoted strings in search currently have no special meaning

        if len(word) > 0:
            value = ''.join(word)
            if key:
                self.parse_search_filter(key, value)
            else:
                search.append(value)  # Quoted strings in search currently have no special meaning

        self.search = " ".join(search)

    def parse_search_filter(self, key, value):
        match key:
            case "status":
                self.status = value
            case "tags":
                self.tags = value
            case "without_tags":
                self.without_tags = value
            case "phase":
                self.phase = value
            case "type":
                self.type = value
            case "department":
                self.department = value
            case "subject_area":
                self.subject_area = value
            case "section":
                self.section = value
            case "visibility":
                self.visibility = value
            case "include_amendments":
                self.include_amendments = value
            case "only_supporting":
                self.only_supporting = value

    def build_search_query(self):
        query = []
        if self.search:
            for word in self.search.split():
                query.append(word)

        if self.status:
            query.append("status:" + self.maybe_add_quotes(self.status))
        if self.tags:
            query.append("tags:" + self.maybe_add_quotes(self.tags))
        if self.without_tags:
            query.append("without_tags:" + self.maybe_add_quotes(self.without_tags))
        if self.phase:
            query.append("phase:" + self.maybe_add_quotes(self.phase))
        if self.type:
            query.append("type:" + self.maybe_add_quotes(self.type))
        if self.department:
            query.append("department:" + self.maybe_add_quotes(self.department))
        if self.subject_area:
            query.append("subject_area:" + self.maybe_add_quotes(self.subject_area))
        if self.section:
            query.append("section:" + self.maybe_add_quotes(self.section))
        if self.visibility:
            query.append("visibility:" + self.maybe_add_quotes(self.visibility))
        if self.include_amendments:
            query.append("include_amendments:" + self.include_amendments)
        if self.only_supporting:
            query.append("only_supporting:" + self.only_supporting)

        return " ".join(query)

    @staticmethod
    def maybe_add_quotes(value):
        if " " in value or ":" in value or '"' in value or "'" in value:
            if '"' in value:
                value = f"'{value}'"
            else:
                value = f'"{value}"'

        return value

    @log_call
    def propositions(self, q, current_user, is_admin=False, count=False):

        Message.log(
            message_type="propositions_filters",
            is_admin=is_admin,
            section=self.section,
            status_values=self.status_values,
            visibility_values=self.visibility_values,
            tag_values=self.tag_values,
            without_tag_values=self.without_tag_values,
        )

        if is_admin and self.visibility_values:
            propositions = q(Proposition).filter(Proposition.visibility.in_(self.visibility_values))
        elif is_admin:
            # Admins see everything when no visibility filter is given
            propositions = q(Proposition)
        else:
            # Normal users only see public propositions
            propositions = q(Proposition).filter_by(visibility=PropositionVisibility.PUBLIC)

        # Search
        if self.search:
            propositions = sqlalchemy_searchable.search(propositions, self.search, sort=True)

        # Filters
        if self.status:
            propositions = propositions.filter(Proposition.status.in_(self.status_values))

        if self.tags:

            tags = q(Tag).filter(func.lower(Tag.name).in_(self.tag_values)).all()

            if len(tags) != len(self.tag_values):
                propositions = propositions.filter(False)
            else:
                for tag in tags:
                    propositions = propositions.filter(Proposition.tags.contains(tag))

        if self.section:
            propositions = propositions.join(Changeset).filter_by(section=self.section)

        # Filters based on ballot
        if self.phase or self.type or self.department:
            propositions = propositions.join(Ballot)

            if self.phase:
                propositions = propositions.join(VotingPhase).filter(
                    func.lower(VotingPhase.name) == func.lower(self.phase)
                )

            if self.type:
                propositions = propositions.join(PropositionType).filter(
                    func.lower(PropositionType.abbreviation) == func.lower(self.type)
                )

            if self.department:
                propositions = propositions.join(SubjectArea)
                if self.subject_area:
                    propositions = propositions.filter(func.lower(SubjectArea.name) == func.lower(self.subject_area))

                propositions = propositions.join(Department).filter(
                    func.lower(Department.name) == func.lower(self.department)
                )

        if self.without_tag_values:
            tags = q(Tag).filter(func.lower(Tag.name).in_(self.without_tag_values)).all()
            for tag in tags:
                propositions = propositions.filter(~Proposition.tags.contains(tag))

        if not self.include_amendments:
            propositions = propositions.filter(Proposition.modifies_id.is_(None))

        if self.only_supporting:
            propositions = (
                propositions.join(Supporter).filter(Supporter.member_id == current_user.id
                                                    ).filter(Supporter.status == SupporterStatus.ACTIVE)
            )

        if count:
            propositions = propositions.count()
        else:

            propositions = propositions.options(
                joinedload(Proposition.ballot),
                joinedload(Proposition.derivations),
                joinedload(Proposition.replacements),
                joinedload(Proposition.proposition_tags),
                joinedload(Proposition.propositions_member),
                joinedload(Proposition.propositions_member),
                joinedload(Proposition.proposition_arguments),
            )

            # Order
            if self.sort == "supporter_count":
                propositions = propositions.order_by(desc(Proposition.active_supporter_count))
            elif self.sort == "date":
                # Use submit date if not null, else use created date.
                propositions = propositions.order_by(desc(coalesce(Proposition.submitted_at, Proposition.created_at)))

            propositions = propositions.order_by(Proposition.voting_identifier, Proposition.title)

            # per_page == -1 => show all on one page
            if self.per_page is None or self.per_page >= 0:
                propositions = propositions.limit(self.propositions_per_page()).offset(
                    ((self.page or 1) - 1) * self.propositions_per_page()
                )

        return propositions

    def to_dict(self):
        return dataclasses.asdict(self)

    def replace(self, **changes):
        return dataclasses.replace(self, **changes)

    def propositions_per_page(self):
        return self.per_page or 20
