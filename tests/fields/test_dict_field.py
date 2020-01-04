"""Dictionary field tests."""
from typing import Any

from pofy import DictField
from pofy import ErrorCode
from pofy import StringField

from tests.fixtures import check_field
from tests.fixtures import check_field_error


class _DictObject:
    class Schema:
        """Pofy fields."""

        dict_field = DictField(StringField())


def _check_dict_field(yaml_value: str, expected_value: dict) -> Any:
    check_field(_DictObject, 'dict_field', yaml_value, expected_value)


def _check_dict_field_error(yaml_value: str, expected_error: ErrorCode) -> Any:
    check_field_error(_DictObject, 'dict_field', yaml_value, expected_error)


def test_dict_field() -> Any:
    """Test dict field loads correct values."""
    _check_dict_field(
        '\n  key_1: value_1'
        '\n  key_2: value_2',
        {'key_1': 'value_1', 'key_2': 'value_2'}
    )

    # A loading failure on an item shouldn't set the corresponding key
    _check_dict_field(
        '\n  key_1: !fail value_1'
        '\n  key_2: value_2',
        {'key_2': 'value_2'}
    )


def test_dict_field_error_handling() -> Any:
    """Test BoolField error handling behaves correctly."""
    _check_dict_field_error('["a", "list"]', ErrorCode.UNEXPECTED_NODE_TYPE)
    _check_dict_field_error('scalar_value', ErrorCode.UNEXPECTED_NODE_TYPE)
