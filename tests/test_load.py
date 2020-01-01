"""Yaml object loading tests."""
from pytest import raises

from pyyo import load
from pyyo import PyyoError
from pyyo import ErrorCode

from tests.fixtures import RequiredFieldObject
from tests.fixtures import SubObjectChild
from tests.fixtures import YamlObject


def test_unknown_field_raise_error():
    """Test an undeclared field in YAML raises an error."""
    error_raised = False

    def _on_error(___, code, __):
        nonlocal error_raised
        error_raised = True
        assert code == ErrorCode.FIELD_NOT_DECLARED

    load(YamlObject, 'uknown_field: 10', error_handler=_on_error)
    assert error_raised


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
