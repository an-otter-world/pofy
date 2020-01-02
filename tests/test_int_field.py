"""Integer field tests."""
from pofy import ErrorCode
from pofy import load

from .fixtures import YamlObject
from .fixtures import expect_load_error


def test_int_field():
    """Test integer field loading works."""
    test = load(YamlObject, 'int_field: 10')
    assert test.int_field == 10


def test_int_field_bad_value_raises():
    """Test integer field bad value raises an error."""
    expect_load_error(
        ErrorCode.VALUE_ERROR,
        YamlObject,
        'int_field: not_convertible'
    )
