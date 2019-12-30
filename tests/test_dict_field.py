"""List field tests."""
from pyyo import DictField
from pyyo import StringField
from pyyo import load

class _Test:
    class Meta:
        """Yaml Fields."""
        string_dict = DictField(StringField())

def test_dict_field():
    """Test dict field deserialization works."""
    test = load(_Test, (
        'string_dict:\n' +
        '  key_1: value_1\n' +
        '  key_2: value_2'
    ))
    assert test.string_dict == {'key_1': 'value_1', 'key_2': 'value_2'}
