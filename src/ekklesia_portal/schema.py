from colander import SchemaNode, MappingSchema, \
    Int, String, Boolean, List, Tuple, \
    Length, OneOf

def string_property(**kwargs):
    return SchemaNode(String(), **kwargs)


def int_property(**kwargs):
    return SchemaNode(Int(), **kwargs)


def bool_property(**kwargs):
    return SchemaNode(Boolean(), **kwargs)


def list_property(**kwargs):
    return SchemaNode(List(), **kwargs)


class PropositionSchema(MappingSchema):
    title = string_property(validator=Length(min=5, max=512))
    short = string_property(validator=Length(min=5, max=2048))
    content = string_property(validator=Length(min=10, max=65536))
    motivation = string_property(missing='')
    tags = list_property(missing=tuple())
    relation_type = string_property(validator=OneOf(['replaces', 'modifies']), missing=None)
    related_proposition_id = int_property(missing=None)


class ArgumentSchema(MappingSchema):
    title = string_property(validator=Length(min=5, max=80))
    abstract = string_property(validator=Length(min=5, max=140))
    details = string_property(validator=Length(min=10, max=4096), missing='')


class ArgumentForPropositionSchema(ArgumentSchema):
    proposition_id = int_property()
    relation_type = string_property(validator=OneOf(['pro', 'con']))
