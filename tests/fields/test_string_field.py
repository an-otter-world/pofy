"""String field tests."""
from pofy.common import ErrorCode
from pofy.fields.string_field import StringField

from tests.helpers import check_field
from tests.helpers import check_field_error


class _StringObject:

    class Schema:
        """Pofy fields."""

        field = StringField(pattern='^matching$')


def _check_field(yml_value: str, expected_value: str) -> None:
    check_field(_StringObject, 'field', yml_value, expected_value)


def _check_field_error(yml_value: str, expected_error: ErrorCode) -> None:
    check_field_error(_StringObject, 'field', yml_value, expected_error)


def test_string_field() -> None:
    """String field should load correct values."""
    _check_field('matching', 'matching')


def test_string_field_error_handling() -> None:
    """String field should correctly handle errors."""
    _check_field_error('[a, list]', ErrorCode.UNEXPECTED_NODE_TYPE)
    _check_field_error('{a: dict}', ErrorCode.UNEXPECTED_NODE_TYPE)

    _check_field_error('not_matching', ErrorCode.VALIDATION_ERROR)
