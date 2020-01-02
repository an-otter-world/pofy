"""List field class & utilities."""
from gettext import gettext as _

from yaml import SequenceNode

from pofy.errors import ErrorCode

from .base_field import BaseField


class ListField(BaseField):
    """List YAML object field."""

    def __init__(self, item_field: BaseField, *args, **kwargs):
        """Initialize the list field.

        Arg:
            item_field: Field used to load list items.
            *args, **kwargs: Arguments forwarded to BaseField.

        """
        super().__init__(*args, **kwargs)
        self._item_field = item_field

    def _load(self, context):
        node = context.current_node()
        if not isinstance(node, SequenceNode):
            context.error(
                ErrorCode.UNEXPECTED_NODE_TYPE,
                _('Sequence expected')
            )
            return None

        result = []
        for item_node in node.value:
            with context.load(item_node) as loaded:
                if not loaded:
                    continue

                item = self._item_field.load(context)
                result.append(item)

        return result
