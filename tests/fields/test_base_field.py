"""Yaml object loading tests."""
from pofy import ErrorCode
from pofy import LoadingContext
from pofy import StringField

from tests.fixtures import expect_load_error


def test_field_validation():
    """Test custom field validaton works."""
    def _validate(context: LoadingContext, _: str):
        context.error(ErrorCode.VALIDATION_ERROR, 'Test')
        return False

    class _ValidateFieldObject:

        class Schema:
            """Pofy fields."""

            validated_field = StringField(validate=_validate)

    expect_load_error(
        ErrorCode.VALIDATION_ERROR,
        _ValidateFieldObject,
        'validated_field: error_is_always_raised',
    )
