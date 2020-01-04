"""Integer field tests."""
from pofy import ErrorCode
from pofy import IntField

from tests.fixtures import check_field
from tests.fixtures import check_field_error


class _IntObject:

    class Schema:
        """Pofy fields."""

        field = IntField(minimum=10, maximum=20)
        hex_field = IntField(base=16)


def _check_field(field: str, yml_value: str, expected_value: int) -> None:
    check_field(_IntObject, field, yml_value, expected_value)


def _check_field_error(
    field: str,
    yml_value: str,
    expected_error: ErrorCode
) -> None:
    check_field_error(_IntObject, field, yml_value, expected_error)


def test_int_field() -> None:
    """Int field should load correct values."""
    _check_field('field', '15', 15)
    _check_field('field', '0xF', 0xF)
    _check_field('field', '0o20', 0o20)
    _check_field('hex_field', 'F00D00FAFA', 0xF00D00FAFA)


def test_int_field_error_handling() -> None:
    """Int field should correctly handle errors."""
    _check_field_error('field', '[a, list]', ErrorCode.UNEXPECTED_NODE_TYPE)
    _check_field_error('field', '{a: dict}', ErrorCode.UNEXPECTED_NODE_TYPE)

    _check_field_error('field', 'bad_value', ErrorCode.VALUE_ERROR)

    # Out of bounds
    _check_field_error('field', '0', ErrorCode.VALIDATION_ERROR)
    _check_field_error('field', '100', ErrorCode.VALIDATION_ERROR)
