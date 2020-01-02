"""Integer field tests."""
from pofy import ErrorCode
from pofy import IntField
from pofy import load

from tests.fixtures import expect_load_error


class _IntObject:

    class Schema:
        """Pofy fields."""

        int_field = IntField()
        hex_int_field = IntField(base=16)
        bounded_int_field = IntField(minimum=10, maximum=20)


def test_int_field():
    """Test integer field loading works."""
    test = load('int_field: 10', _IntObject)
    assert test.int_field == 10

    test = load('int_field: 0xF00D00FAFA', _IntObject)
    assert test.int_field == 0xF00D00FAFA

    test = load('int_field: 0o42', _IntObject)
    assert test.int_field == 0o42


def test_int_field_bad_value_raises():
    """Test integer field bad value raises an error."""
    expect_load_error(
        ErrorCode.VALUE_ERROR,
        'int_field: not_convertible',
        _IntObject,
    )


def test_int_field_base():
    """Test integer field base parameter works."""
    test = load('hex_int_field: F00D00FAFA', _IntObject)
    assert test.hex_int_field == 0xF00D00FAFA


def test_int_field_min_max():
    """Test integer field minimum / maximum parameter works."""
    expect_load_error(
        ErrorCode.VALIDATION_ERROR,
        'bounded_int_field: 0',
        _IntObject,
    )

    expect_load_error(
        ErrorCode.VALIDATION_ERROR,
        'bounded_int_field: 100',
        _IntObject,
    )
