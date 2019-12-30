"""String field tests."""
from pyyo import load
from pyyo import IntField

def test_int():
    """Test number field deserialization works."""
    class _Test:
        class Meta:
            """Yaml Fields."""
            test_field = IntField()

    test = load(_Test, 'test_field: 10')
    assert test.test_field == 10
