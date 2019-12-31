"""String field tests."""
from pytest import raises

from pyyo import load
from pyyo import ParseError

from .fixtures import YamlObject


def test_string_field():
    """Test string field deserialization works."""
    test = load(YamlObject, 'string_field: test_value')
    assert test.string_field == 'test_value'


def test_bad_value_raises():
    """Test not-scalar field raise an error."""
    with raises(ParseError):
        load(YamlObject, 'string_field: ["a", "list"]')
