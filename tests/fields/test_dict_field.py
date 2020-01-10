"""Dictionary field tests."""

from pofy import DictField
from pofy import ErrorCode
from pofy import StringField

from tests.helpers import check_field
from tests.helpers import check_field_error


class _DictObject:
    class Schema:
        """Pofy fields."""

        field = DictField(StringField())


def _check_field(yaml_value: str, expected_value: dict) -> None:
    check_field(_DictObject, 'field', yaml_value, expected_value)


def _check_field_error(yaml_value: str, expected_error: ErrorCode) -> None:
    check_field_error(_DictObject, 'field', yaml_value, expected_error)


def test_dict_field() -> None:
    """Dict field should load correct values."""
    _check_field(
        '{key_1: value_1, key_2: value_2}',
        {'key_1': 'value_1', 'key_2': 'value_2'}
    )

    # A loading failure on an item shouldn't set the corresponding key
    _check_field(
        '{key_1: !fail value_1, key_2: value_2}',
        {'key_2': 'value_2'}
    )


def test_dict_field_error_handling() -> None:
    """Dict field should correctly handle errors."""
    _check_field_error('scalar_value', ErrorCode.UNEXPECTED_NODE_TYPE)
    _check_field_error('[a, list]', ErrorCode.UNEXPECTED_NODE_TYPE)
