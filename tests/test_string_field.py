"""String field tests."""
from pytest import raises

from pyyo import ParseError
from pyyo import StringField
from pyyo import YamlObject

class _Test(YamlObject):
    test_field = StringField()

def test_string_field():
    """Test string field deserialization works."""
    test = _Test('test_field: test_value')
    assert test.test_field == 'test_value'

def test_bad_value_raises():
    """Test not-scalar field raise an error."""
    with raises(ParseError):
        _Test('test_field: ["a", "list"]')
