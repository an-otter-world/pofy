"""List field tests."""
from pofy import ErrorCode
from pofy import load

from .fixtures import YamlObject
from .fixtures import expect_load_error


def test_list_field():
    """Test list field loading works."""
    test = load(YamlObject, 'list_field: ["value_1", "value_2" ]')
    assert test.list_field == ['value_1', 'value_2']


def test_list_field_error_on_bad_node():
    """Test list field loading raises an error on bad node."""
    expect_load_error(
        ErrorCode.UNEXPECTED_NODE_TYPE,
        YamlObject,
        'list_field:\n' +
        '  key_1: value_1\n' +
        '  key_2: value_2'
    )
