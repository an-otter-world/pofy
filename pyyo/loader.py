"""Pyyo deserializing function."""

from gettext import gettext as _
from inspect import getmembers
from inspect import isclass
from io import StringIO
from yaml import MappingNode
from yaml import Node
from yaml import compose

from .fields.base_field import BaseField
from .errors import parse_error

def load(object_class, source):
    """Deserializes a YAML document into an object."""
    node = __load_yaml(source)
    fields = dict(__get_fields(object_class))

    if not isinstance(node, MappingNode):
        parse_error(node, _('Expected a mapping.'))

    result = object_class()
    for name_node, value_node in node.value:
        field_name = name_node.value
        if not field_name in fields:
            parse_error(name_node, _('Unknown field {}'), field_name)

        field = fields[field_name]
        field_value = field.deserialize(value_node)
        setattr(result, field_name, field_value)

    return result

def __get_fields(cls):
    def _is_meta_class(member):
        return isclass(member) and member.__name__ == 'Meta'

    def _is_field(member):
        return isinstance(member, BaseField)

    for _, metaclass in getmembers(cls, _is_meta_class):
        for name, field in getmembers(metaclass, _is_field):
            yield (name, field)

def __load_yaml(source):
    if isinstance(source, Node):
        return source

    if source is str:
        return compose(StringIO(source))

    return compose(source)
