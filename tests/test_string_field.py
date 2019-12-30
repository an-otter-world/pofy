"""String field tests."""
from pytest import raises

from pyyo import ParseError
from pyyo import StringField
from pyyo import deserialize

class _Test:
    class Meta:
        """Yaml Fields."""
        test_field = StringField()

def test_string_field():
    """Test string field deserialization works."""
    test = deserialize('test_field: test_value', _Test)
    assert test.test_field == 'test_value'

def test_bad_value_raises():
    """Test not-scalar field raise an error."""
    with raises(ParseError):
        deserialize('test_field: ["a", "list"]', _Test)
