"""Object field tests."""
from pyyo import load

from .fixtures import TestObject
from .fixtures import TestSubObject


def test_object_field():
    """Test object field deserialization works."""
    test = load(TestObject, (
        'object_field:\n' +
        '  string_field: field_value\n'
    ))
    assert isinstance(test.sub_object, TestSubObject)
    assert test.sub_object.string_field == 'field_value'
