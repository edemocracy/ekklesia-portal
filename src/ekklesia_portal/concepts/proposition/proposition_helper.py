from operator import attrgetter
from ekklesia_common.translation import _
from ekklesia_portal.enums import PropositionStatus


def items_for_proposition_select_widgets(departments, tags, selected_tags=None):
    area_items = []

    for department in sorted(departments, key=attrgetter('name')):
        for area in sorted(department.areas, key=attrgetter('name')):
            area_items.append((area.id, f"{department.name} - {area.name}"))

    status_items = [(e.name, _('_'.join(['proposition_status', e.value]))) for e in PropositionStatus]

    tag_items = [(t.name, t.name) for t in tags]

    if selected_tags is not None:
        tag_names_to_create = set(selected_tags) - set(t.name for t in tags)
        tag_items.extend((t, t) for t in tag_names_to_create)

    return {'area': area_items, 'status': status_items, 'tags': tag_items}
