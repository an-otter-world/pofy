"""Yaml object tests."""
from pytest import raises

from pyyo import load
from pyyo import ParseError

from tests.fixtures import YamlObject
from tests.fixtures import RequiredFieldObject


def test_unknown_field_raise_error():
    """Test an undeclared field in YAML raises an error."""
    with raises(ParseError):
        load(YamlObject, 'uknown_field: 10')


def test_unset_required_field_raise_error():
    """Test an unset required field in YAML raise an error."""
    with raises(ParseError):
        load(RequiredFieldObject, 'not_required: some_value')

    test = load(RequiredFieldObject, (
        'required: setted\n'
        'not_required: yodeldi'
    ))
    assert test.required == 'setted'
    assert test.not_required == 'yodeldi'
