"""List field tests."""
from pofy import ErrorCode
from pofy import ListField
from pofy import StringField
from pofy import load

from tests.fixtures import expect_load_error
from tests.fixtures import load_with_fail_tag


class _ListObject:

    class Schema:
        """Pofy fields."""

        list_field = ListField(StringField())


def test_list_field():
    """Test list field loading works."""
    test = load(_ListObject, 'list_field: ["value_1", "value_2" ]')
    assert test.list_field == ['value_1', 'value_2']


def test_list_field_error_on_bad_node():
    """Test list field loading raises an error on bad node."""
    expect_load_error(
        ErrorCode.UNEXPECTED_NODE_TYPE,
        _ListObject,
        'list_field:\n' +
        '  key_1: value_1\n' +
        '  key_2: value_2'
    )


def test_list_field_ignores_tag_handler_failure():
    """Test dict field loading raises an error on bad node."""
    test = load_with_fail_tag(_ListObject, (
        'list_field:\n' +
        '- !fail value_1\n' +
        '- value_2'
    ))

    assert test.list_field == ['value_2']
