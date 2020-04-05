"""Enum field class & utilities."""
from enum import Enum
from gettext import gettext as _
from typing import Any
from typing import Optional
from typing import Type

from pofy.common import ErrorCode
from pofy.common import LOADING_FAILED
from pofy.fields.base_field import ScalarField
from pofy.fields.base_field import ValidateCallback
from pofy.interfaces import ILoadingContext


class EnumField(ScalarField):
    """Enum YAML object field."""

    def __init__(
        self,
        enum_class: Type[Enum],
        required: bool = False,
        validate: Optional[ValidateCallback] = None
    ):
        """Initialize string field.

        Args:
            enum_class: The type of the enum to deserialize.
            required: See BaseField constructor.
            validate: See BaseField constructor.

        """
        super().__init__(required=required, validate=validate)
        self._enum_class = enum_class

    def _convert(self, context: ILoadingContext) -> Any:
        string_value = context.current_node().value

        for member in self._enum_class:
            if member.name == string_value:
                return member

        context.error(
            ErrorCode.VALIDATION_ERROR,
            _('Unkown value {} for enum {}.'),
            string_value,
            self._enum_class
        )
        return LOADING_FAILED
