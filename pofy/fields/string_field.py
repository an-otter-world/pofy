"""String field class & utilities."""
from gettext import gettext as _
from re import compile as re_compile
from typing import Any
from typing import Optional
from typing import Pattern

from pofy.common import ErrorCode
from pofy.common import LOADING_FAILED
from pofy.fields.base_field import ScalarField
from pofy.fields.base_field import ValidateCallback
from pofy.interfaces import ILoadingContext


class StringField(ScalarField):
    """String YAML object field."""

    def __init__(
        self,
        required: bool = False,
        validate: Optional[ValidateCallback] = None,
        pattern: Optional[str] = None
    ):
        """Initialize string field.

        Args:
            required: See BaseField constructor.
            validate: See BaseField constructor.
            pattern: Pattern the deserialized strings should match. If defined
                     and the string doesn't match, a VALIDATION_ERROR will be
                     raised.

        """
        super().__init__(required=required, validate=validate)
        self._pattern_str: Optional[str] = None
        self._pattern: Optional[Pattern[str]] = None

        if pattern is not None:
            assert isinstance(pattern, str), \
                _('pattern must be a string.')
            self._pattern_str = pattern
            self._pattern = re_compile(pattern)

    def _convert(self, context: ILoadingContext) -> Any:
        value = context.current_node().value

        if self._pattern is not None and not self._pattern.match(value):
            context.error(
                ErrorCode.VALIDATION_ERROR,
                _('Value {} doesn\'t match required pattern {}'),
                value,
                self._pattern_str
            )
            return LOADING_FAILED

        return value
