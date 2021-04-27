import colander
from operator import attrgetter

from ekklesia_common.translation import _

from ekklesia_portal.enums import VotingType
from ekklesia_portal.concepts.voting_phase import voting_phase_helper


def items_for_ballot_select_widgets(ballot, departments, proposition_types):
    area_items = [('', _('not_determined'))]
    voting_phase_items = [('', _('not_determined'))]

    for department in sorted(departments, key=attrgetter('name')):
        for area in sorted(department.areas, key=attrgetter('name')):
            area_items.append((area.id, f"{department.name} - {area.name}"))

        for voting_phase in department.voting_phases:
            if voting_phase.ballots_can_be_added:
                voting_phase_title = voting_phase_helper.voting_phase_title(voting_phase)
                voting_phase_items.append((voting_phase.id, f'{department.name} - {voting_phase_title}'))

    proposition_type_items = [('', _('not_determined'))] + [(t.id, t.name) for t in proposition_types]
    voting_type_items = [("", _('not_determined'))] + [(e.name, _('_'.join(['voting_type', e.value]))) for e in VotingType]
    return {
        'area': area_items,
        'proposition_type': proposition_type_items,
        'voting': voting_phase_items,
        'voting_type': voting_type_items
    }
