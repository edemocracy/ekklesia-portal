class InvalidVotingModule(KeyError):
    pass


def prepare_module_config(app, department, voting_module_name):
    department_overrides = department.voting_module_settings.get(voting_module_name)
    if department_overrides is None:
        raise InvalidVotingModule(f"Module {voting_module_name} is not a valid voting module for {department.name}")

    from_config = {**getattr(app.settings.voting_modules, voting_module_name)}
    defaults = from_config.pop("defaults")
    return {**from_config, **defaults, **department_overrides}
