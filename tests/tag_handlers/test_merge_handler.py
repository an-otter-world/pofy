"""If handler tests."""
from typing import Any
from typing import Optional

from pofy.common import ErrorCode
from pofy.common import LOADING_FAILED
from pofy.fields.base_field import BaseField
from pofy.fields.dict_field import DictField
from pofy.fields.list_field import ListField
from pofy.fields.string_field import StringField
from pofy.tag_handlers.merge_handler import MergeHandler

from tests.helpers import check_load


def _check_merge_tag(
    field: BaseField,
    yaml: str,
    expected_value: Any = None,
    expected_error: Optional[ErrorCode] = None
) -> None:
    if expected_error is not None:
        expected_value = LOADING_FAILED

    result = check_load(
        yaml,
        field=field,
        tag_handlers=[
            MergeHandler()
        ],
        expected_error=expected_error
    )

    assert result == expected_value


def test_if_tag_handler() -> None:
    """Env tag should correctly load sequences of list or dicts."""
    # Merging list should work
    _check_merge_tag(
        ListField(StringField()),
        '!merge [[value_1, value_2], [value_3]]',
        ['value_1', 'value_2', 'value_3']
    )

    # Merging dicts should work
    _check_merge_tag(
        DictField(StringField()),
        '!merge [{a: a_value, b: b_value}, {b: overwrite_b}]',
        {'a': 'a_value', 'b': 'overwrite_b'}
    )

    # An undefined value in the sequence should be ignored
    _check_merge_tag(
        ListField(StringField()),
        '!merge [[value_1, value_2], !fail [value_3]]',
        ['value_1', 'value_2']
    )

    # An empty sequence should return UNDEFINED
    _check_merge_tag(
        ListField(StringField()),
        '!merge []',
        LOADING_FAILED
    )


def test_merge_tag_handler_error_handling() -> None:
    """Switch tag should correctly handle errors."""
    _check_merge_tag(
        ListField(StringField()),
        '!merge scalar_value',
        expected_error=ErrorCode.UNEXPECTED_NODE_TYPE
    )

    _check_merge_tag(
        ListField(StringField()),
        '!merge {}',
        expected_error=ErrorCode.UNEXPECTED_NODE_TYPE
    )

    _check_merge_tag(
        StringField(),
        '!merge [scalar_value]',
        expected_error=ErrorCode.VALUE_ERROR
    )
