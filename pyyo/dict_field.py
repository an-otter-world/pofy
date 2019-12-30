"""List field class & utilities."""
from gettext import gettext as _

from yaml import MappingNode
from yaml import ScalarNode

from .parse_error import parse_error
from .base_field import BaseField

class DictField(BaseField):
    """Dict YAML object field."""

    def __init__(self, item_field):
        """Initialize dict field.

        Arg:
            item_field (pyyo.BaseField) : Field used to deserialize dictionnary
                                          entry values.
        """
        self._item_field = item_field

    def deserialize(self, node):
        """See pyyo.BaseField.deserialize for usage."""
        if not isinstance(node, MappingNode):
            parse_error(node, _('Expected a mapping'))

        result = {}
        for key_node, value_node in node.value:
            assert isinstance(key_node, ScalarNode)
            key = key_node.value
            result[key] = self._item_field.deserialize(value_node)

        return result
