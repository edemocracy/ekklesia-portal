from ekklesia_common.translation import _

from ekklesia_portal.enums import VotingStatus


def items_for_voting_phase_select_widgets(phase_types, departments, voting_phase=None):
    status_items = [(e.name, _('_'.join(['voting_status', e.value]))) for e in VotingStatus]

    phase_type_items = [(pt.id, pt.name) for pt in phase_types]
    department_items = [(d.id, d.name) for d in departments]

    return {'status': status_items, 'phase_type': phase_type_items, 'department': department_items}


def voting_phase_title(voting_phase):
    return voting_phase.name or (f'{voting_phase.phase_type.name} #{voting_phase.id}')
