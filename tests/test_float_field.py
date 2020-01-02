"""Float field tests."""
from pofy import ErrorCode
from pofy import load

from .fixtures import YamlObject
from .fixtures import expect_load_error


def test_float_field():
    """Test float field loading works."""
    test = load(YamlObject, 'float_field: 42.2')
    assert test.float_field == 42.2


def test_float_field_bad_value_raises():
    """Test bad value on a float field raises an error."""
    expect_load_error(
        ErrorCode.VALUE_ERROR,
        YamlObject,
        'float_field: not_convertible'
    )


def test_float_field_min_max():
    """Test float field minimum / maximum parameter works."""
    expect_load_error(
        ErrorCode.VALIDATION_ERROR,
        YamlObject,
        'bounded_float_field: 0.0'
    )

    expect_load_error(
        ErrorCode.VALIDATION_ERROR,
        YamlObject,
        'bounded_float_field: 100.0'
    )
