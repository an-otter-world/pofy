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
    test = load(_IntObject, 'int_field: 10')
    assert test.int_field == 10

    test = load(_IntObject, 'int_field: 0xF00D00FAFA')
    assert test.int_field == 0xF00D00FAFA

    test = load(_IntObject, 'int_field: 0o42')
    assert test.int_field == 0o42


def test_int_field_bad_value_raises():
    """Test integer field bad value raises an error."""
    expect_load_error(
        ErrorCode.VALUE_ERROR,
        _IntObject,
        'int_field: not_convertible'
    )


def test_int_field_base():
    """Test integer field base parameter works."""
    test = load(_IntObject, 'hex_int_field: F00D00FAFA')
    assert test.hex_int_field == 0xF00D00FAFA


def test_int_field_min_max():
    """Test integer field minimum / maximum parameter works."""
    expect_load_error(
        ErrorCode.VALIDATION_ERROR,
        _IntObject,
        'bounded_int_field: 0'
    )

    expect_load_error(
        ErrorCode.VALIDATION_ERROR,
        _IntObject,
        'bounded_int_field: 100'
    )
