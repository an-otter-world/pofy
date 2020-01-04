"""String field tests."""
from pofy import BoolField
from pofy import ErrorCode

from tests.fixtures import check_field
from tests.fixtures import check_field_error


class _BoolObject:
    """Test class for bool field tests."""

    class Schema:
        """Pofy fields."""

        field = BoolField()


def _check_field(yaml_value: str, expected_value: bool):
    check_field(_BoolObject, 'field', yaml_value, expected_value)


def _check_field_error(yaml_value: str, expected_error: ErrorCode):
    check_field_error(_BoolObject, 'field', yaml_value, expected_error)


def test_bool_field() -> None:
    """Bool field should load correct values."""
    true_values = [
        'y', 'Y', 'yes', 'Yes', 'YES',
        'true', 'True', 'TRUE',
        'on', 'On', 'ON'
    ]

    for value in true_values:
        _check_field(value, True)

    false_values = [
        'n', 'N', 'no', 'No', 'NO',
        'false', 'False', 'FALSE'
        'off', 'Off', 'OFF'
    ]

    for value in false_values:
        _check_field(value, False)


def test_bool_field_error_handling() -> None:
    """Bool field should correctly handle errors."""
    _check_field_error('[a, list]', ErrorCode.UNEXPECTED_NODE_TYPE)
    _check_field_error('{a: dict}', ErrorCode.UNEXPECTED_NODE_TYPE)

    _check_field_error('bad_value', ErrorCode.VALUE_ERROR)
