"""String field tests."""
from enum import Enum

from pofy.common import ErrorCode
from pofy.fields.enum_field import EnumField

from tests.helpers import check_field
from tests.helpers import check_field_error


class _TestEnum(Enum):
    FIRST = 10
    SECOND = 20
    THIRD = 30


class _EnumObject:

    class Schema:
        """Pofy fields."""

        field = EnumField(enum_class=_TestEnum)


def _check_field(yml_value: str, expected_value: _TestEnum) -> None:
    check_field(_EnumObject, 'field', yml_value, expected_value)


def _check_field_error(yml_value: str, expected_error: ErrorCode) -> None:
    check_field_error(_EnumObject, 'field', yml_value, expected_error)


def test_enum_field() -> None:
    """String field should load correct values."""
    _check_field('FIRST', _TestEnum.FIRST)
    _check_field('SECOND', _TestEnum.SECOND)
    _check_field('THIRD', _TestEnum.THIRD)


def test_enum_field_error_handling() -> None:
    """String field should correctly handle errors."""
    _check_field_error('[a, list]', ErrorCode.UNEXPECTED_NODE_TYPE)
    _check_field_error('{a: dict}', ErrorCode.UNEXPECTED_NODE_TYPE)

    _check_field_error('BAD_ENUM', ErrorCode.VALIDATION_ERROR)
