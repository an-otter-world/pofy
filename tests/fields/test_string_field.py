"""String field tests."""
from pofy import ErrorCode
from pofy import StringField
from pofy import load

from tests.fixtures import expect_load_error


class _StringObject:

    class Schema:
        """Pofy fields."""

        string_field = StringField()
        match_string_field = StringField(pattern='^Matching$')


def test_string_field():
    """Test string field loading works."""
    test = load('string_field: test_value', _StringObject)
    assert test.string_field == 'test_value'


def test_bad_value_raises():
    """Test not-scalar node for a string field raise an error."""
    expect_load_error(
        ErrorCode.UNEXPECTED_NODE_TYPE,
        'string_field: ["a", "list"]',
        _StringObject
    )


def test_pattern():
    """Test string validates pattern when given."""
    test = load(
        'match_string_field: Matching',
        _StringObject,
    )
    assert test.match_string_field == 'Matching'

    expect_load_error(
        ErrorCode.VALIDATION_ERROR,
        'match_string_field: NotMatching',
        _StringObject,
    )
