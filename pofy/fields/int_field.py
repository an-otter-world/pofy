"""Integer field class & utilities."""
from gettext import gettext as _

from pofy.errors import ErrorCode

from .base_field import ScalarField


class IntField(ScalarField):
    """Integer YAML object field."""

    def __init__(self, *args, base: int = 0, **kwargs):
        """Initialize int field.

        Args:
            base: Base in which this field is encoded. By default, base is 0,
                  meaning that python will distinguish automatically decimal,
                  octal, and hexadecimal notations from the string.
            *args, **kwargs : Arguments forwarded to ScalarField.

        """
        super().__init__(*args, **kwargs)
        self._base = base

    def _convert(self, node, context):
        value = node.value
        try:
            return int(value, self._base)
        except ValueError:
            context.error(
                node,
                ErrorCode.VALUE_ERROR,
                _('Can\'t convert "{}" to an integer'), value
            )

        return None
