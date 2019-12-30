"""String field tests."""
from io import StringIO

from pyyo import IntField
from pyyo import YamlObject

def test_int():
    """Test number field deserialization works."""
    class _Test(YamlObject):
        class Meta:
            """Yaml Fields."""
            test_field = IntField()

    stream = StringIO('test_field: 10')

    test = _Test(stream)
    assert test.test_field == 10
