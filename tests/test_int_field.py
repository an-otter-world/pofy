"""Integer field tests."""
from pofy import load

from .fixtures import YamlObject


def test_int():
    """Test integer field loading works."""
    test = load(YamlObject, 'int_field: 10')
    assert test.int_field == 10
