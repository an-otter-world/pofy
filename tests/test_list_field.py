"""List field tests."""
from io import StringIO

from pyyo import ListField
from pyyo import StringField
from pyyo import YamlObject

class _Test(YamlObject):
    string_list = ListField(StringField())

def test_int():
    """Test list field deserialization works."""
    test = _Test('string_list: ["value_1", "value_2" ]')
    assert test.string_list == ['value_1', 'value_2']
