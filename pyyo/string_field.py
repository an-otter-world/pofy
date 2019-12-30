"""String field class & utilities."""
from .base_field import ScalarField

class StringField(ScalarField):
    """String YAML object field."""

    def _convert(self, value):
        return value
