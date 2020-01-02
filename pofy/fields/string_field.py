"""String field class & utilities."""
from gettext import gettext as _
from re import compile as re_compile
from typing import AnyStr

from pofy.errors import ErrorCode

from .base_field import ScalarField


class StringField(ScalarField):
    """String YAML object field."""

    def __init__(self, *args, pattern: AnyStr = None, **kwargs):
        """Initialize string field.

        Args:
            pattern: Pattern the deserialized strings should match. If defined
                     and the string doesn't match, a VALIDATION_ERROR will be
                     raised.
            *args, **kwargs: arguments forwarded to ScalarField.

        """
        super().__init__(*args, **kwargs)

        if pattern is not None:
            self._pattern_str = pattern
            self._pattern = re_compile(pattern)
        else:
            self._pattern_str = None
            self._pattern = None

    def _convert(self, context):
        value = context.current_node().value

        if self._pattern is not None and not self._pattern.match(value):
            context.error(
                ErrorCode.VALIDATION_ERROR,
                _('Value {} doesn\'t match required pattern {}'),
                value,
                self._pattern_str
            )
            return None

        return value
