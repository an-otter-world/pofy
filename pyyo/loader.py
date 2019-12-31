"""Pyyo deserializing function."""

from gettext import gettext as _
from inspect import getmembers
from inspect import isclass
from io import StringIO
from typing import IO
from typing import Type
from typing import List
from typing import Union

from yaml import compose
from yaml import MappingNode
from yaml import Node

from .errors import parse_error
from .loading_context import LoadingContext
from .fields.base_field import BaseField
from .resolvers import Resolver


def load(
    cls: Type,
    source: Union[str, IO[str], Node],
    resolvers: List[Resolver] = None
) -> object:
    """Deserialize a YAML document into an object."""
    node = _load_yaml(source)
    context = LoadingContext(resolvers)
    return load_internal(cls, node, context)


def load_internal(object_class: Type, node: Node, context: LoadingContext):
    """Load given node.

    This function is meant to be used internaly, by ObjectField and load.
    """
    fields = dict(_get_fields(object_class))

    if not isinstance(node, MappingNode):
        parse_error(node, _('Expected a mapping.'))

    result = object_class()
    set_fields = set()
    for name_node, value_node in node.value:
        field_name = name_node.value
        set_fields.add(field_name)
        if field_name not in fields:
            parse_error(name_node, _('Unknown field {}'), field_name)

        field = fields[field_name]
        field_value = field.load(value_node, context)
        setattr(result, field_name, field_value)

    for name, field in fields.items():
        if field.required and name not in set_fields:
            parse_error(node, _('Missing required field {}'), name)

    return result


def _get_fields(cls):
    def _is_schema_class(member):
        return isclass(member) and member.__name__ == 'Schema'

    def _is_field(member):
        return isinstance(member, BaseField)

    for __, schemaclass in getmembers(cls, _is_schema_class):
        for name, field in getmembers(schemaclass, _is_field):
            yield (name, field)


def _load_yaml(source):
    if isinstance(source, Node):
        return source

    if source is str:
        return compose(StringIO(source))

    return compose(source)
