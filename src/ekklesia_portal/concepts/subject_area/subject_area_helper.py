def items_for_subject_area_select_widgets(departments):
    department_items = [(d.id, d.name) for d in departments]

    return {'department': department_items}

