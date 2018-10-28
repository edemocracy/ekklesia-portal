def items_for_proposition_type_select_widgets(policies):
    policy_items = [(p.id, p.name) for p in policies]
    return {'policy': policy_items}
