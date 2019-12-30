"""List field tests."""
from pyyo import DictField
from pyyo import StringField
from pyyo import deserialize

class _Test:
    class Meta:
        """Yaml Fields."""
        string_dict = DictField(StringField())

def test_dict_field():
    """Test dict field deserialization works."""
    test = deserialize((
        'string_dict:\n' +
        '  key_1: value_1\n' +
        '  key_2: value_2'
    ), _Test)
    assert test.string_dict == {'key_1': 'value_1', 'key_2': 'value_2'}
