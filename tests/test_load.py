"""Yaml object tests."""
from pytest import raises

from pyyo import load
from pyyo import ParseError


def test_unknown_field_raise_error():
    """Test an undeclared field in YAML raises an error."""
    with raises(ParseError):
        load(object, 'uknown_field: 10')
