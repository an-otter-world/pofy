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
    test = load('float_field: 42.2', _FloatObject)
    assert test.float_field == 42.2


def test_float_field_bad_value_raises():
    """Test bad value on a float field raises an error."""
    result = expect_load_error(
        ErrorCode.VALUE_ERROR,
        'float_field: not_convertible',
        _FloatObject,
    )
    assert not hasattr(result, 'float_field')


def test_float_field_min_max():
    """Test float field minimum / maximum parameter works."""
    result = expect_load_error(
        ErrorCode.VALIDATION_ERROR,
        'bound_float_field: 0.0',
        _FloatObject,
    )
    assert not hasattr(result, 'bound_float_field')

    result = expect_load_error(
        ErrorCode.VALIDATION_ERROR,
        'bound_float_field: 100.0',
        _FloatObject,
    )
    assert not hasattr(result, 'bound_float_field')

    result = load('bound_float_field: 17.2', _FloatObject)
    assert result.bound_float_field == 17.2
