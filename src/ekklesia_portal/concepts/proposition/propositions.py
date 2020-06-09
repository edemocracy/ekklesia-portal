import dataclasses
from dataclasses import dataclass
from ekklesia_portal.database.datamodel import Proposition, Ballot, VotingPhase, PropositionStatus, PropositionType, SubjectArea, Department, Tag
from sqlalchemy import desc, func
from sqlalchemy_searchable import search


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
    tag: str = None
    type: str = None

    def __post_init__(self):
        self.parse_search_filters()

        # Force None value if argument is empty to clean up url
        self.department = self.department or None
        self.document = self.document or None
        self.phase = self.phase or None
        self.search = self.search or None
        self.section = self.section or None
        self.sort = self.sort or None
        self.tag = self.tag or None
        self.type = self.type or None

        try:
            self.status = PropositionStatus(self.status.lower() if self.status else None)
        except ValueError:
            self.status = None

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
        for c in self.search.strip():
            if c == '"' or c == '\'':
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
        if key == "status":
            self.status = value
        elif key == "tag":
            self.tag = value
        elif key == "phase":
            self.phase = value
        elif key == "type":
            self.type = value
        elif key == "department":
            self.department = value
        elif key == "subject_area":
            self.subject_area = value

    def build_search_query(self):
        query = []
        if self.search:
            for word in self.search.split():
                query.append(word)

        if self.status:
            query.append("status:" + self.maybe_add_quotes(self.status))
        if self.tag:
            query.append("tag:" + self.maybe_add_quotes(self.tag))
        if self.phase:
            query.append("phase:" + self.maybe_add_quotes(self.phase))
        if self.type:
            query.append("type:" + self.maybe_add_quotes(self.type))
        if self.department:
            query.append("department:" + self.maybe_add_quotes(self.department))
        if self.subject_area:
            query.append("subject_area:" + self.maybe_add_quotes(self.subject_area))

        return " ".join(query)

    @staticmethod
    def maybe_add_quotes(value):
        if " " in value or ":" in value or '"' in value or "'" in value:
            if '"' in value:
                value = f"'{value}'"
            else:
                value = f'"{value}"'

        return value

    def propositions(self, q):
        propositions = q(Proposition)

        # Search
        if self.search:
            propositions = search(propositions, self.search, sort=True)

        # Filters
        if self.status:
            propositions = propositions.filter_by(status=self.status)

        if self.tag:
            propositions = propositions.join(*Proposition.tags.attr).filter(func.lower(Tag.name) == func.lower(self.tag))

        # Filters based on ballot
        if self.phase or self.type or self.department:
            propositions = propositions.join(Ballot)

            if self.phase:
                propositions = propositions.join(VotingPhase).filter(func.lower(VotingPhase.name) == func.lower(self.phase))

            if self.type:
                propositions = propositions.join(PropositionType).filter(func.lower(PropositionType.abbreviation) == func.lower(self.type))

            if self.department:
                propositions = propositions.join(SubjectArea)
                if self.subject_area:
                    propositions = propositions.filter(func.lower(SubjectArea.name) == func.lower(self.subject_area))

                propositions = propositions.join(Department).filter(func.lower(Department.name) == func.lower(self.department))

        # Order
        if self.sort == "supporter_count":
            propositions = propositions.order_by(desc(Proposition.active_supporter_count))

        propositions = propositions.order_by(Proposition.voting_identifier, Proposition.title)

        return propositions

    def to_dict(self):
        return dataclasses.asdict(self)

    def replace(self, **changes):
        return dataclasses.replace(self, **changes)
