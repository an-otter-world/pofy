"""Integer field class & utilities."""
from .base_field import ScalarField


class IntField(ScalarField):
    """Integer YAML object field."""

    def _convert(self, node, context):
        return int(node.value)
