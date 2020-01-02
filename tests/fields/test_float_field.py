"""Float field tests."""
from pofy import ErrorCode
from pofy import FloatField
from pofy import load

from tests.fixtures import expect_load_error


class _FloatObject:

    class Schema:
        """Pofy fields."""

        float_field = FloatField()
        bound_float_field = FloatField(minimum=10.0, maximum=20.0)


def test_float_field():
    """Test float field loading works."""
    test = load(_FloatObject, 'float_field: 42.2')
    assert test.float_field == 42.2


def test_float_field_bad_value_raises():
    """Test bad value on a float field raises an error."""
    expect_load_error(
        ErrorCode.VALUE_ERROR,
        _FloatObject,
        'float_field: not_convertible'
    )


def test_float_field_min_max():
    """Test float field minimum / maximum parameter works."""
    expect_load_error(
        ErrorCode.VALIDATION_ERROR,
        _FloatObject,
        'bound_float_field: 0.0'
    )

    expect_load_error(
        ErrorCode.VALIDATION_ERROR,
        _FloatObject,
        'bound_float_field: 100.0'
    )

    test = load(_FloatObject, 'bound_float_field: 17.2')
    assert test.bound_float_field == 17.2