"""List field class & utilities."""
from gettext import gettext as _
from typing import Any
from typing import Optional

from pofy.common import LOADING_FAILED
from pofy.fields.base_field import BaseField
from pofy.fields.base_field import ValidateCallback
from pofy.interfaces import ILoadingContext


class ListField(BaseField):
    """List YAML object field."""

    def __init__(
        self,
        item_field: BaseField,
        required: bool = False,
        validate: Optional[ValidateCallback] = None,
    ):
        """Initialize the list field.

        Arg:
            item_field: Field used to load list items.
            required: See BaseField constructor.
            validate: See BaseField constructor.

        """
        super().__init__(required=required, validate=validate)
        assert isinstance(item_field, BaseField), \
            _('item_field must be an implementation of BaseField.')
        self._item_field = item_field

    def _load(self, context: ILoadingContext) -> Any:
        if not context.expect_sequence():
            return LOADING_FAILED

        node = context.current_node()
        result = []
        for item_node in node.value:
            item = context.load(self._item_field, item_node)
            if item is LOADING_FAILED:
                continue

            result.append(item)

        return result
