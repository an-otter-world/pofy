"""Boolean field class & utilities."""
from gettext import gettext as _

from pofy.errors import ErrorCode

from .base_field import ScalarField


class BoolField(ScalarField):
    """Boolean YAML object field."""

    def _convert(self, node, context):
        true_values = [
            'y', 'Y', 'yes', 'Yes', 'YES',
            'true', 'True', 'TRUE',
            'on', 'On', 'ON'
        ]
        false_values = [
            'n', 'N', 'no', 'No', 'NO',
            'false', 'False', 'FALSE'
            'off', 'Off', 'OFF'
        ]

        value = node.value
        if value in true_values:
            return True

        if value in false_values:
            return False

        context.error(
            node,
            ErrorCode.VALUE_ERROR,
            _('Boolean value should be one of {}'),
            ', '.join(true_values + false_values)
        )

        return None
