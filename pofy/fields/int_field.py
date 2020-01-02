"""Integer field class & utilities."""
from gettext import gettext as _

from pofy.errors import ErrorCode

from .base_field import ScalarField


class IntField(ScalarField):
    """Integer YAML object field."""

    def _convert(self, node, context):
        value = node.value
        try:
            return int(value)
        except ValueError:
            context.error(
                node,
                ErrorCode.VALUE_ERROR,
                _('Can\'t convert "{}" to an integer'), value
            )

        return None
