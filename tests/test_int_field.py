"""String field tests."""
from pyyo import load

from .fixtures import YamlObject


def test_int():
    """Test number field deserialization works."""
    test = load(YamlObject, 'int_field: 10')
    assert test.int_field == 10
