"""Float field tests."""
from pofy import ErrorCode
from pofy import FloatField

from tests.fixtures import check_field
from tests.fixtures import check_field_error


class _FloatObject:

    class Schema:
        """Pofy fields."""

        float_field = FloatField(minimum=10.0, maximum=20.0)


def _check_float_field(yml_value: str, expected_value: float) -> None:
    check_field(_FloatObject, 'float_field', yml_value, expected_value)


def _check_float_field_error(yml_value: str, expected_error: ErrorCode) -> None:
    check_field_error(_FloatObject, 'float_field', yml_value, expected_error)


def test_float_field() -> None:
    """Test float field loads correct values."""
    _check_float_field('17.2', 17.2)


def test_bool_field_error_handling() -> None:
    """Test BoolField error handling behaves correctly."""
    _check_float_field_error('not_convertible', ErrorCode.VALUE_ERROR)

    # Out of bounds
    _check_float_field_error('0.0', ErrorCode.VALIDATION_ERROR)
    _check_float_field_error('100.0', ErrorCode.VALIDATION_ERROR)
