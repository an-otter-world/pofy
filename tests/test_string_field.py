"""String field tests."""
from pytest import raises

from pyyo import ParseError
from pyyo import StringField
from pyyo import load

class _Test:
    class Meta:
        """Yaml Fields."""
        test_field = StringField()

def test_string_field():
    """Test string field deserialization works."""
    test = load(_Test, 'test_field: test_value')
    assert test.test_field == 'test_value'

def test_bad_value_raises():
    """Test not-scalar field raise an error."""
    with raises(ParseError):
        load(_Test, 'test_field: ["a", "list"]')
