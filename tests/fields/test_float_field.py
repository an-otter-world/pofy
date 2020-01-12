"""Float field tests."""
from pofy.common import ErrorCode
from pofy.fields.float_field import FloatField

from tests.helpers import check_field
from tests.helpers import check_field_error


class _FloatObject:

    class Schema:
        """Pofy fields."""

        field = FloatField(minimum=10.0, maximum=20.0)


def _check_field(yml_value: str, expected_value: float) -> None:
    check_field(_FloatObject, 'field', yml_value, expected_value)


def _check_field_error(yml_value: str, expected_error: ErrorCode) -> None:
    check_field_error(_FloatObject, 'field', yml_value, expected_error)


def test_float_field() -> None:
    """Float field should load correct values."""
    _check_field('17.2', 17.2)


def test_float_field_error_handling() -> None:
    """Float field should correctly handle errors."""
    _check_field_error('[a, list]', ErrorCode.UNEXPECTED_NODE_TYPE)
    _check_field_error('{a: dict}', ErrorCode.UNEXPECTED_NODE_TYPE)

    _check_field_error('bad_value', ErrorCode.VALUE_ERROR)

    # Out of bounds
    _check_field_error('0.0', ErrorCode.VALIDATION_ERROR)
    _check_field_error('100.0', ErrorCode.VALIDATION_ERROR)
