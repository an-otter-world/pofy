"""Float field class & utilities."""
from gettext import gettext as _
from typing import Any
from typing import Optional

from pofy.common import ErrorCode
from pofy.common import LOADING_FAILED
from pofy.fields.base_field import ScalarField
from pofy.interfaces import ILoadingContext


class FloatField(ScalarField):
    """Float YAML object field."""

    def __init__(
        self,
        *args,
        minimum: Optional[float] = None,
        maximum: Optional[float] = None,
        **kwargs
    ):
        """Initialize float field.

        Args:
            minimum: Minimum value for the field. If the value is out of bound,
                     a VALIDATION_ERROR will be raised.
            maximum: Maximum value for the field. If the value is out of bound,
                     a VALIDATION_ERROR will be raised.
            *args, **kwargs : Arguments forwarded to ScalarField.

        """
        super().__init__(*args, **kwargs)
        self._minimum: Optional[float] = minimum
        self._maximum: Optional[float] = maximum

    def _convert(self, context: ILoadingContext) -> Any:
        node = context.current_node()
        value = node.value
        try:
            result = float(value)
        except ValueError:
            context.error(
                ErrorCode.VALUE_ERROR,
                _('Can\'t convert "{}" to a float'), value
            )
            return LOADING_FAILED

        return ScalarField._check_in_bounds(
            context,
            result,
            self._minimum,
            self._maximum
        )
