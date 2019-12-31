"""List field class & utilities."""
from gettext import gettext as _

from yaml import MappingNode
from yaml import ScalarNode

from pyyo.errors import parse_error

from .base_field import BaseField


class DictField(BaseField):
    """Dict YAML object field."""

    def __init__(self, item_field: BaseField, *args, **kwargs):
        """Initialize dict field.

        Arg:
            item_field (pyyo.BaseField) : Field used to load dictionnary
                                          entry values.
            *args, **kwargs (list, dict) : Arguments forwarded to BaseField.

        """
        super().__init__(*args, **kwargs)
        self._item_field = item_field

    def _load(self, node, context):
        """See pyyo.BaseField.load for usage."""
        if not isinstance(node, MappingNode):
            parse_error(node, _('Expected a mapping'))

        result = {}
        for key_node, value_node in node.value:
            assert isinstance(key_node, ScalarNode)
            key = key_node.value
            result[key] = self._item_field.load(value_node, context)

        return result
