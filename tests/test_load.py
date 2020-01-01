"""Yaml object loading tests."""
from io import StringIO

from pytest import raises
from yaml import compose

from pyyo import load
from pyyo import PyyoError
from pyyo import Resolver

from tests.fixtures import RequiredFieldObject
from tests.fixtures import SubObjectChild
from tests.fixtures import YamlObject


def test_unknown_field_raise_error():
    """Test an undeclared field in YAML raises an error."""
    with raises(PyyoError):
        load(YamlObject, 'uknown_field: 10')


def test_unset_required_field_raise_error():
    """Test an unset required field in YAML raise an error."""
    with raises(PyyoError):
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


def test_loading_subclass_works():
    """Test fields declared in parent classes are loaded."""
    test = load(
        SubObjectChild,
        'test_field: parent_value\n' +
        'child_field: child_value',
    )
    assert test.test_field == 'parent_value'
    assert test.child_field == 'child_value'
