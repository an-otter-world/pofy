"""Number field class & utilities."""
from .base_field import ScalarField

class IntField(ScalarField):
    """Number YAML object field."""

    def _convert(self, value):
        return int(value)
