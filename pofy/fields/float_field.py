"""Float field class & utilities."""
from .base_field import ScalarField


class FloatField(ScalarField):
    """Float YAML object field."""

    def _convert(self, node, context):
        return float(node.value)
