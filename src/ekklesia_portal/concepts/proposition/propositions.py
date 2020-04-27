from ekklesia_portal.database.datamodel import Proposition, Ballot, VotingPhase, PropositionStatus, PropositionType, SubjectArea, Department
from sqlalchemy import desc
from sqlalchemy_searchable import search


class Propositions:
    def __init__(self, mode=None, search=None, tag=None, phase=None, type=None, status=None, department=None, subject_area=None):
        self.search = search
        self.mode = mode
        self.tag = tag
        self.phase = phase
        self.type = type

        self.status = None
        if status and status in set(item.value for item in PropositionStatus):
            self.status = status

        self.department = department
        self.subject_area = None
        if department:  # Don't display subject area filter when no department filter is given
            self.subject_area = subject_area

    def propositions(self, q):
        propositions = q(Proposition)

        # Search
        if self.search:
            propositions = search(propositions, self.search, sort=True)

        # Filters
        if self.status:
            propositions = propositions.filter_by(status=PropositionStatus(self.status))

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
        if self.mode == "top":
            propositions = propositions.order_by(desc(Proposition.active_supporter_count))

        elif self.mode == "sorted":
            propositions = propositions.order_by(Proposition.voting_identifier, Proposition.title)

        elif self.mode == "custom":
            raise NotImplementedError()

        return propositions

    def to_dict(self):
        return {
            'search': self.search,
            'mode': self.mode,
            'tag': self.tag,
            'phase': self.phase,
            'type': self.type,
            'status': self.status,
            'department': self.department,
            'subject_area': self.subject_area
        }
