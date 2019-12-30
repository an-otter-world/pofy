"""Yaml object tests."""
from pytest import raises

from pyyo import ParseError
from pyyo import YamlObject

def test_unknown_field_raise_error():
    """Test an undeclared field in YAML raises an error."""
    with raises(ParseError):
        YamlObject('uknown_field: 10')
