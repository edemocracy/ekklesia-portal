from eliot import start_action
from ekklesia_portal import voting_modules


class InvalidVotingModule(KeyError):
    pass


def prepare_module_config(app, department, voting_module_name):
    try:
        (create_voting, retrieve_voting) = voting_modules.VOTING_MODULES[voting_module_name]
    except KeyError:
        raise InvalidVotingModule(f"Unsupported voting module {voting_module_name}")

    with start_action(action_type="get_voting_module_settings", voting_module_setttings=department.voting_module_settings):
        department_overrides = department.voting_module_settings.get(voting_module_name)
    if department_overrides is None:
        raise InvalidVotingModule(f"Module {voting_module_name} is not a valid voting module for {department.name}")

    from_config = {**getattr(app.settings.voting_modules, voting_module_name)}
    defaults = from_config.pop("defaults")
    return {**from_config, **defaults, **department_overrides, "create_voting": create_voting, "retrieve_voting": retrieve_voting}
