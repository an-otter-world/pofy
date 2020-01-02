"""Integer field class & utilities."""
from gettext import gettext as _
from typing import Optional

from pofy.errors import ErrorCode

from .base_field import ScalarField


class IntField(ScalarField):
    """Integer YAML object field."""

    def __init__(
        self,
        *args,
        base: int = 0,
        minimum: Optional[int] = None,
        maximum: Optional[int] = None,
        **kwargs
    ):
        """Initialize int field.

        Args:
            base: Base in which this field is encoded. By default, base is 0,
                  meaning that python will distinguish automatically decimal,
                  octal, and hexadecimal notations from the string.
            minimum: Minimum value for the field. If the value is out of bound,
                     a VALIDATION_ERROR will be raised.
            maximum: Maximum value for the field. If the value is out of bound,
                     a VALIDATION_ERROR will be raised.
            *args, **kwargs : Arguments forwarded to ScalarField.

        """
        super().__init__(*args, **kwargs)
        self._base = base
        self._minimum = minimum
        self._maximum = maximum

    def _convert(self, node, context):
        value = node.value
        try:
            result = int(value, self._base)
        except ValueError:
            context.error(
                node,
                ErrorCode.VALUE_ERROR,
                _('Can\'t convert "{}" to an integer'), value
            )
            return None

        return ScalarField._check_in_bounds(
            node,
            context,
            result,
            self._minimum,
            self._maximum
        )
