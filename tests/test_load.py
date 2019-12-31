"""Yaml object tests."""
from pytest import raises

from pyyo import load
from pyyo import ParseError

from tests.fixtures import YamlObject


def test_unknown_field_raise_error():
    """Test an undeclared field in YAML raises an error."""
    with raises(ParseError):
        load(YamlObject, 'uknown_field: 10')
