"""String field tests."""
from pyyo import load

from .fixtures import TestObject


def test_int():
    """Test number field deserialization works."""
    test = load(TestObject, 'test_field: 10')
    assert test.test_field == 10
