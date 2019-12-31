"""List field tests."""
from pyyo import load

from .fixtures import YamlObject


def test_int():
    """Test list field deserialization works."""
    test = load(YamlObject, 'list_field: ["value_1", "value_2" ]')
    assert test.list_field == ['value_1', 'value_2']
