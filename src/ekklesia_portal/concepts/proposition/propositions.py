import dataclasses
from dataclasses import dataclass
from ekklesia_portal.database.datamodel import Proposition, Ballot, VotingPhase, PropositionStatus, PropositionType, SubjectArea, Department
from sqlalchemy import desc
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
            self.status = PropositionStatus(self.status)
        except ValueError:
            self.status = None

        # Don't display subject area filter when no department filter is given
        self.subject_area = self.subject_area if self.department and self.subject_area else None

    def propositions(self, q):
        propositions = q(Proposition)

        # Search
        if self.search:
            propositions = search(propositions, self.search, sort=True)

        # Filters
        if self.status:
            propositions = propositions.filter_by(status=self.status)

        if self.tag:
            propositions = propositions.join(*Proposition.tags.attr).filter_by(name=self.tag)

        # Filters based on ballot
        if self.phase or self.type or self.department:
            propositions = propositions.join(Ballot)

            if self.phase:
                propositions = propositions.join(VotingPhase).filter_by(name=self.phase)

            if self.type:
                propositions = propositions.join(PropositionType).filter_by(abbreviation=self.type)

            if self.department:
                propositions = propositions.join(SubjectArea)
                if self.subject_area:
                    propositions = propositions.filter_by(name=self.subject_area)

                propositions = propositions.join(Department).filter_by(name=self.department)

        # Order
        if self.sort == "supporter_count":
            propositions = propositions.order_by(desc(Proposition.active_supporter_count))

        propositions = propositions.order_by(Proposition.voting_identifier, Proposition.title)

        return propositions

    def to_dict(self):
        return dataclasses.asdict(self)

    def replace(self, **changes):
        return dataclasses.replace(self, **changes)
