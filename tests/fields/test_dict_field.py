"""Dictionary field tests."""
from pofy import DictField
from pofy import ErrorCode
from pofy import StringField
from pofy import load

from tests.fixtures import expect_load_error


class _DictObject:
    class Schema:
        """Pofy fields."""

        dict_field = DictField(StringField())


def test_dict_field():
    """Test dict field loading works."""
    test = load(_DictObject, (
        'dict_field:\n' +
        '  key_1: value_1\n' +
        '  key_2: value_2'
    ))
    assert test.dict_field == {'key_1': 'value_1', 'key_2': 'value_2'}


def test_dict_field_error_on_bad_node():
    """Test dict field loading raises an error on bad node."""
    expect_load_error(
        ErrorCode.UNEXPECTED_NODE_TYPE,
        _DictObject,
        'dict_field:\n' +
        '  - key_1\n' +
        '  - key_2'
    )
