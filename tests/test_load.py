"""Yaml object loading tests."""
from pytest import raises

from pyyo import load
from pyyo import PyyoError
from pyyo import ErrorCode

from .fixtures import RequiredFieldObject
from .fixtures import SubObjectChild
from .fixtures import YamlObject
from .fixtures import expect_load_error


def test_unknown_field_raise_error():
    """Test an undeclared field in YAML raises an error."""
    expect_load_error(
        ErrorCode.FIELD_NOT_DECLARED,
        YamlObject,
        'uknown_field: 10'
    )


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


def test_load_subclass():
    """Test fields declared in parent classes are loaded."""
    test = load(
        SubObjectChild,
        'test_field: parent_value\n' +
        'child_field: child_value',
    )
    assert test.test_field == 'parent_value'
    assert test.child_field == 'child_value'
