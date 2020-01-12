"""List field tests."""
from typing import List
from typing import Optional

from pofy.common import ErrorCode
from pofy.fields.list_field import ListField
from pofy.fields.string_field import StringField

from tests.helpers import check_field
from tests.helpers import check_field_error


class _ListObject:

    class Schema:
        """Pofy fields."""

        field = ListField(StringField())

    def __init__(self) -> None:
        """Initialize _ListObject."""
        self.field: Optional[List[str]] = None


def _check_field(yaml_value: str, expected_value: List[str]) -> None:
    check_field(_ListObject, 'field', yaml_value, expected_value)


def _check_field_error(yaml_value: str, expected_error: ErrorCode) -> None:
    check_field_error(_ListObject, 'field', yaml_value, expected_error)


def test_list_field() -> None:
    """List field should load correct values."""
    _check_field('[ item1, item2 ]', ['item1', 'item2'])

    # A loading failure on an item shouldn't be added to the list
    _check_field('[ !fail item1, item2 ]', ['item2'])


def test_list_field_error_handling() -> None:
    """List field should correctly handle errors."""
    _check_field_error('scalar_value', ErrorCode.UNEXPECTED_NODE_TYPE)
    _check_field_error('{a, dict}', ErrorCode.UNEXPECTED_NODE_TYPE)
