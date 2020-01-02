"""Yaml object loading tests."""
from pofy import load
from pofy import ErrorCode

from .fixtures import RequiredFieldObject
from .fixtures import SubObject
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
    expect_load_error(
        ErrorCode.MISSING_REQUIRED_FIELD,
        RequiredFieldObject,
        'not_required: some_value'
    )

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


def test_error_on_bad_node():
    """Test load raises an error on bad node."""
    expect_load_error(
        ErrorCode.UNEXPECTED_NODE_TYPE,
        YamlObject,
        '- item1\n' +
        '- item2'
    )


def test_resolve_root_works(datadir):
    """Test giving a path as resolve_root instanciates FileSystemResolvers."""
    test = load(
        YamlObject,
        'object_field: !include object.yaml\n',
        resolve_roots=[datadir]
    )

    assert isinstance(test.object_field, SubObject)
    assert test.object_field.test_field == 'test_value'
