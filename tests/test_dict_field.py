"""Dictionary field tests."""
from pyyo import load

from .fixtures import YamlObject


def test_dict_field():
    """Test dict field loading works."""
    test = load(YamlObject, (
        'dict_field:\n' +
        '  key_1: value_1\n' +
        '  key_2: value_2'
    ))
    assert test.dict_field == {'key_1': 'value_1', 'key_2': 'value_2'}
