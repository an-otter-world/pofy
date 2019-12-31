"""List field tests."""
from pyyo import load

from .fixtures import TestObject


def test_int():
    """Test list field deserialization works."""
    test = load(TestObject, 'list_field: ["value_1", "value_2" ]')
    assert test.string_list == ['value_1', 'value_2']
