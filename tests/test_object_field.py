"""Object field tests."""
from pyyo import load

from .fixtures import YamlObject
from .fixtures import SubObject


def test_object_field():
    """Test object field deserialization works."""
    test = load(YamlObject, (
        'object_field:\n' +
        '  test_field: field_value\n'
    ))
    assert isinstance(test.object_field, SubObject)
    assert test.object_field.test_field == 'field_value'
