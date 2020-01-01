"""String field tests."""
from pytest import raises

from pyyo import load
from pyyo import PyyoError

from .fixtures import YamlObject


def test_string_field():
    """Test string field loading works."""
    test = load(YamlObject, 'string_field: test_value')
    assert test.string_field == 'test_value'


def test_bad_value_raises():
    """Test not-scalar node for a string field raise an error."""
    with raises(PyyoError):
        load(YamlObject, 'string_field: ["a", "list"]')
