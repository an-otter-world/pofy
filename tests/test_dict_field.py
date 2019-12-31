"""List field tests."""
from pyyo import load

from .fixtures import TestObject


def test_dict_field():
    """Test dict field deserialization works."""
    test = load(TestObject, (
        'string_dict:\n' +
        '  key_1: value_1\n' +
        '  key_2: value_2'
    ))
    assert test.string_dict == {'key_1': 'value_1', 'key_2': 'value_2'}
