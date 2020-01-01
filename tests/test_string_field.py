"""String field tests."""
from pytest import raises

from pyyo import load
from pyyo import ErrorCode

from .fixtures import YamlObject
from .fixtures import expect_load_error


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
