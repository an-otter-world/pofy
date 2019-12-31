"""Yaml object tests."""
from io import StringIO

from pytest import raises
from yaml import compose

from pyyo import load
from pyyo import ParseError
from pyyo import Resolver

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


def test_resolve():
    """Test !include tag uses resolver to find YAML documents to load."""
    class _DummyResolver(Resolver):
        def resolve(self, location):
            assert location == 'some_location'
            return compose(StringIO('test_field: test_value'))

    test = load(
        YamlObject,
        'object_field: !include some_location',
        resolvers=[_DummyResolver()]
    )
    assert test.object_field.test_field == 'test_value'
