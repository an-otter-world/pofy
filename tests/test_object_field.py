"""Object field tests."""
from pyyo import load

from .fixtures import YamlObject
from .fixtures import SubObject
from .fixtures import SubObjectChild


def test_object_field():
    """Test object field deserialization works."""
    test = load(YamlObject, (
        'object_field:\n' +
        '  test_field: field_value\n'
    ))
    assert isinstance(test.object_field, SubObject)
    assert test.object_field.test_field == 'field_value'


def test_type_tag():
    """Test specifying a type for an object field works."""
    test = load(YamlObject, (
        'object_field: !type:tests.fixtures.SubObjectChild\n' +
        '  test_field: test_value\n' +
        '  child_field: child_value\n'
    ))
    assert isinstance(test.object_field, SubObjectChild)
    assert test.object_field.test_field == 'test_value'
    assert test.object_field.child_field == 'child_value'
