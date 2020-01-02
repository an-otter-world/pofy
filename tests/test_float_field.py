"""Float field tests."""
from pofy import load

from .fixtures import YamlObject


def test_float_field():
    """Test float field loading works."""
    test = load(YamlObject, 'float_field: 42.2')
    assert test.float_field == 42.2
