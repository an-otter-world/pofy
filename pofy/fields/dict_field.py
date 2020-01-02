"""Dictionary field class & utilities."""
from gettext import gettext as _

from yaml import MappingNode
from yaml import ScalarNode

from pofy.errors import ErrorCode

from .base_field import BaseField


class DictField(BaseField):
    """Dictionary YAML object field."""

    def __init__(self, item_field: BaseField, *args, **kwargs):
        """Initialize dict field.

        Args:
            item_field: Field used to load dictionnary values.
            *args, **kwargs : Arguments forwarded to BaseField.

        """
        super().__init__(*args, **kwargs)
        self._item_field = item_field

    def _load(self, context):
        node = context.current_node()
        if not isinstance(node, MappingNode):
            context.error(
                ErrorCode.UNEXPECTED_NODE_TYPE,
                _('Mapping expected')
            )
            return None

        result = {}
        for key_node, value_node in node.value:
            assert isinstance(key_node, ScalarNode)
            key = key_node.value

            with context.load(value_node) as loaded:
                if not loaded:
                    continue
                result[key] = self._item_field.load(context)

        return result
