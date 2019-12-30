"""String field tests."""
from io import StringIO

from pyyo import NumberField
from pyyo import YamlObject

def test_number_field():
    """Test number field deserialization works."""
    class _Test(YamlObject):
        test_field = NumberField()

    stream = StringIO('test_field: 10')

    test = _Test(stream)
    assert test.test_field == 10

