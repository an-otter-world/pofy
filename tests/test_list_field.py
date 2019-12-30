"""List field tests."""
from pyyo import ListField
from pyyo import StringField
from pyyo import load

class _Test:
    class Meta:
        """Yaml Fields."""
        string_list = ListField(StringField())

def test_int():
    """Test list field deserialization works."""
    test = load(_Test, 'string_list: ["value_1", "value_2" ]')
    assert test.string_list == ['value_1', 'value_2']
