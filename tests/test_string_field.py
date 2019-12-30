"""String field tests."""
from pyyo import StringField
from pyyo import YamlObject

def test_string_field():
    """Test string field deserialization works."""
    class _Test(YamlObject):
        test_field = StringField()

    test = _Test('test_field: test_value')
    assert test.test_field == 'test_value'
