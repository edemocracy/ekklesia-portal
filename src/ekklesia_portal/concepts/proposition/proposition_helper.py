from operator import attrgetter

from slugify import slugify
from ekklesia_common.translation import _

from ekklesia_portal.datamodel import Tag
from ekklesia_portal.enums import PropositionStatus, PropositionVisibility


slug_replacements = [
    ['Ü', 'Ue'], ['ü', 'ue'],
    ['Ö', 'Oe'], ['ö', 'oe'],
    ['Ä', 'Ae'], ['ä', 'ae'],
    ['ß', 'ss']
]


def items_for_proposition_select_widgets(departments, tags, proposition_types=None, selected_tags=None):
    area_items = []

    for department in sorted(departments, key=attrgetter('name')):
        for area in sorted(department.areas, key=attrgetter('name')):
            area_items.append((area.id, f"{department.name} - {area.name}"))

    status_items = [(e.name, _('_'.join(['proposition_status', e.value]))) for e in PropositionStatus]
    visibility_items = [(e.name, _('_'.join(['proposition_visibility', e.value]))) for e in PropositionVisibility]

    tag_items = [(t.name, t.name) for t in tags]

    if selected_tags is not None:
        tag_names_to_create = set(selected_tags) - set(t.name for t in tags)
        tag_items.extend((t, t) for t in tag_names_to_create)

    items = {'area': area_items, 'status': status_items, 'tags': tag_items, 'visibility': visibility_items}

    if proposition_types:
        proposition_type_items = [(t.id, t.name) for t in proposition_types]
        items['proposition_type'] = proposition_type_items

    return items


def get_or_create_tags(db_session, tag_names):
    tags = db_session.query(Tag).filter(Tag.name.in_(tag_names)).all()
    new_tag_names = set(tag_names) - {t.name for t in tags}

    for tag_name in new_tag_names:
        tag = Tag(name=tag_name)
        tags.append(tag)

    return tags


def proposition_slug(proposition):
    return slugify(proposition.title, replacements=slug_replacements)
