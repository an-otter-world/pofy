"""Dictionary field class & utilities."""
from gettext import gettext as _
from typing import Any
from typing import Optional

from yaml import ScalarNode

from pofy.common import UNDEFINED
from pofy.fields.base_field import BaseField
from pofy.fields.base_field import ValidateCallback
from pofy.interfaces import ILoadingContext


class DictField(BaseField):
    """Dictionary YAML object field."""

    def __init__(
        self,
        item_field: BaseField,
        required: bool = False,
        validate: Optional[ValidateCallback] = None,
    ):
        """Initialize dict field.

        Args:
            item_field: Field used to load dictionnary values.
            required: See BaseField constructor.
            validate: See BaseField constructor.

        """
        super().__init__(required=required, validate=validate)
        assert isinstance(item_field, BaseField), \
            _('item_field must be an implementation of BaseField.')
        self._item_field = item_field

    def _load(self, context: ILoadingContext) -> Any:
        node = context.current_node()
        if not context.expect_mapping():
            return UNDEFINED

        result = {}
        for key_node, value_node in node.value:
            assert isinstance(key_node, ScalarNode)
            key = key_node.value

            item = context.load(self._item_field, value_node)
            if item is UNDEFINED:
                continue

            result[key] = item

        return result
