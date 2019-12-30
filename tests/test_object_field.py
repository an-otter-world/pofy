"""Object field tests."""
from pyyo import ObjectField
from pyyo import StringField
from pyyo import YamlObject

class _SubObject(YamlObject):
    string_field = StringField()

class _SubObjectChild(_SubObject):
    child_string_field = StringField()

class _OtherSuboject(YamlObject):
    string_field = StringField()

class _Test(YamlObject):
    sub_object = ObjectField(_SubObject)

def test_object_field():
    """Test object field deserialization works."""
    test = _Test((
        'sub_object:\n' +
        '  string_field: field_value\n'
    ))
    assert isinstance(test.sub_object, _SubObject)
    #pylint: disable=no-member
    assert test.sub_object.string_field == 'field_value'
