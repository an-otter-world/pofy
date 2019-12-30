"""Yaml object tests."""
from pytest import raises

from pyyo import deserialize
from pyyo import ParseError

def test_unknown_field_raise_error():
    """Test an undeclared field in YAML raises an error."""
    with raises(ParseError):
        deserialize('uknown_field: 10', object)
