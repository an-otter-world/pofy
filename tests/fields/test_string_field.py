"""String field tests."""
from pofy import load
from pofy import ErrorCode

from tests.fixtures import YamlObject
from tests.fixtures import expect_load_error


def test_string_field():
    """Test string field loading works."""
    test = load(YamlObject, 'string_field: test_value')
    assert test.string_field == 'test_value'


def test_bad_value_raises():
    """Test not-scalar node for a string field raise an error."""
    expect_load_error(
        ErrorCode.UNEXPECTED_NODE_TYPE,
        YamlObject,
        'string_field: ["a", "list"]'
    )


def test_pattern():
    """Test string validates pattern when given."""
    test = load(
        YamlObject,
        'match_string_field: Matching'
    )
    assert test.match_string_field == 'Matching'

    expect_load_error(
        ErrorCode.VALIDATION_ERROR,
        YamlObject,
        'match_string_field: NotMatching'
    )
