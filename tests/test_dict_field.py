"""Dictionary field tests."""
from pofy import ErrorCode
from pofy import load

from .fixtures import YamlObject
from .fixtures import expect_load_error


def test_dict_field():
    """Test dict field loading works."""
    test = load(YamlObject, (
        'dict_field:\n' +
        '  key_1: value_1\n' +
        '  key_2: value_2'
    ))
    assert test.dict_field == {'key_1': 'value_1', 'key_2': 'value_2'}


def test_dict_field_error_on_bad_node():
    """Test dict field loading raises an error on bad node."""
    expect_load_error(
        ErrorCode.UNEXPECTED_NODE_TYPE,
        YamlObject,
        'dict_field:\n' +
        '  - key_1\n' +
        '  - key_2'
    )
