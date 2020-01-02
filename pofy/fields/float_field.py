"""Float field class & utilities."""
from gettext import gettext as _

from pofy.errors import ErrorCode

from .base_field import ScalarField


class FloatField(ScalarField):
    """Float YAML object field."""

    def _convert(self, node, context):
        value = node.value
        try:
            return float(value)
        except ValueError:
            context.error(
                node,
                ErrorCode.VALUE_ERROR,
                _('Can\'t convert "{}" to a float'), value
            )

        return None
