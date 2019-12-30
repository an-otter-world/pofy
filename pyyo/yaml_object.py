"""Base deserialilable YAML object class & utilities."""
from gettext import gettext as _
from inspect import getmembers
from io import StringIO
from yaml import MappingNode
from yaml import Node
from yaml import compose

from .base_field import BaseField
from .parse_error import parse_error

class YamlObject:
    """Base class for YAML deserializable object."""

    def __init__(self, source):
        """Initialize YamlObject.

        source can be a string, a stream or directly a yaml.Node. If a string
        or a stream is given, it will be parsed as a YAML document.

        Args:
            source (str, stream, yaml.Node) : Either a string, a stream to
                                              or a yaml.Node used to
        """
        yaml_node = YamlObject.__load_yaml(source)
        self.__load(yaml_node)

    @staticmethod
    def __load_yaml(source):
        if source is Node:
            return source

        if source is str:
            return compose(StringIO(source))

        return compose(source)

    def __load(self, node):
        fields = dict(self._get_fields())

        if not isinstance(node, MappingNode):
            parse_error(node, _('Expected a mapping.'))

        for name_node, value_node in node.value:
            field_name = name_node.value
            if not field_name in fields:
                parse_error(name_node, _('Unknown field {}'), field_name)

            field = fields[field_name]
            field_value = field.deserialize(value_node)
            setattr(self, field_name, field_value)

    @classmethod
    def _get_fields(cls):
        def _is_field(member):
            return isinstance(member, BaseField)

        for name, field in getmembers(cls, _is_field):
            yield (name, field)
