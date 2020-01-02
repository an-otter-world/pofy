"""String field tests."""
from pofy import load
from pofy import ErrorCode

from tests.fixtures import YamlObject
from tests.fixtures import expect_load_error


def test_bool_field():
    """Test bool field loading works."""
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
            YamlObject,
            'bool_field: {}'.format(value)
        )

        assert isinstance(test.bool_field, bool)
        assert test.bool_field

    for value in false_values:
        test = load(
            YamlObject,
            'bool_field: {}'.format(value)
        )

        assert isinstance(test.bool_field, bool)
        assert not test.bool_field


def test_bad_value_raises():
    """Test not-scalar node for a string field raise an error."""
    expect_load_error(
        ErrorCode.VALUE_ERROR,
        YamlObject,
        'bool_field: NotValid'
    )

    expect_load_error(
        ErrorCode.UNEXPECTED_NODE_TYPE,
        YamlObject,
        'bool_field: ["a", "list"]'
    )
