"""Yaml object loading tests."""
from pofy.common import ErrorCode
from pofy.fields.string_field import StringField
from pofy.interfaces import ILoadingContext

from tests.helpers import check_field_error


def test_field_validation() -> None:
    """Custom field validation should behave correctly."""
    def _validate(context: ILoadingContext, _: str) -> bool:
        context.error(ErrorCode.VALIDATION_ERROR, 'Test')
        return False

    class _ValidateFieldObject:

        class Schema:
            """Pofy fields."""

            validated_field = StringField(validate=_validate)

    check_field_error(
        _ValidateFieldObject,
        'validated_field',
        'value',
        ErrorCode.VALIDATION_ERROR
    )
