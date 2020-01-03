"""List field class & utilities."""
from gettext import gettext as _
from typing import Optional

from pofy.loading_context import LoadingContext

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
        assert isinstance(item_field, BaseField), \
            _('item_field must be an implementation of BaseField.')
        self._item_field = item_field

    def _load(self, context: LoadingContext) -> Optional[list]:
        if not context.expect_sequence():
            return None

        node = context.current_node()
        result = []
        for item_node in node.value:
            with context.load(item_node) as loaded:
                if not loaded:
                    continue

                item = self._item_field.load(context)
                result.append(item)

        return result
