"""String field tests."""
from io import StringIO

from pyyo import deserialize
from pyyo import IntField

def test_int():
    """Test number field deserialization works."""
    class _Test:
        class Meta:
            """Yaml Fields."""
            test_field = IntField()

    test = deserialize('test_field: 10', _Test)
    assert test.test_field == 10
