"""String field tests."""
from pofy import BoolField
from pofy import ErrorCode
from pofy import load

from tests.fixtures import expect_field_error


class _BoolObject:
    """Test class for bool field tests."""

    class Schema:
        """Pofy fields."""

        bool_field = BoolField()


def test_bool_field():
    """Test bool field loads correct values."""
    true_values = [
        'y', 'Y', 'yes', 'Yes', 'YES',
        'true', 'True', 'TRUE',
        'on', 'On', 'ON'
    ]
    false_values = [
        'n', 'N', 'no', 'No', 'NO',
        'false', 'False', 'FALSE'
        'off', 'Off', 'OFF'
    ]

    for value in true_values:
        test = load(
            'bool_field: {}'.format(value),
            _BoolObject,
        )

        assert isinstance(test.bool_field, bool)
        assert test.bool_field

    for value in false_values:
        test = load(
            'bool_field: {}'.format(value),
            _BoolObject,
        )

        assert isinstance(test.bool_field, bool)
        assert not test.bool_field


def test_bool_field_error_handling():
    """Test BoolField error handling behaves correctly."""
    expect_field_error(
        _BoolObject,
        'bool_field', 'NotValidValue',
        ErrorCode.VALUE_ERROR
    )

    expect_field_error(
        _BoolObject,
        'bool_field', '["a", "list"]',
        ErrorCode.UNEXPECTED_NODE_TYPE
    )
