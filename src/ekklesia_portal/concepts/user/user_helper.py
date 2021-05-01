def items_for_user_select_widgets(groups):
    group_items = [(g.name, g.name) for g in groups]

    return {
        'groups': group_items
    }
