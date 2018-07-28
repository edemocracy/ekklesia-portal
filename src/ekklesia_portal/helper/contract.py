from colander import SchemaNode, MappingSchema, \
    Int, String, Boolean, List


def string_property(**kwargs):
    return SchemaNode(String(), **kwargs)


def int_property(**kwargs):
    return SchemaNode(Int(), **kwargs)


def bool_property(**kwargs):
    return SchemaNode(Boolean(), **kwargs)


def list_property(**kwargs):
    return SchemaNode(List(), **kwargs)


class Schema(MappingSchema):
    pass
