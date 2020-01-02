"""Object field tests."""
from pofy import load
from pofy import ErrorCode

from tests.fixtures import SubObject
from tests.fixtures import SubObjectChild
from tests.fixtures import YamlObject
from tests.fixtures import expect_load_error


def test_object_field():
    """Test object field loading works."""
    test = load(YamlObject, (
        'object_field:\n' +
        '  test_field: field_value\n'
    ))
    assert isinstance(test.object_field, SubObject)
    assert test.object_field.test_field == 'field_value'


def test_object_field_error_on_bad_node():
    """Test object field loading raises an error on bad node."""
    expect_load_error(
        ErrorCode.UNEXPECTED_NODE_TYPE,
        YamlObject,
        'object_field:\n' +
        '  - item1\n' +
        '  - item2'
    )


def test_type_tag():
    """Test specifying a type for an object field works."""
    test = load(YamlObject, (
        'object_field: !type:tests.fixtures.SubObjectChild\n' +
        '  test_field: test_value\n' +
        '  child_field: child_value\n'
    ))
    assert isinstance(test.object_field, SubObjectChild)
    assert test.object_field.test_field == 'test_value'
    assert test.object_field.child_field == 'child_value'


def test_bad_type_raise_error():
    """Test a type tag not existing or not pointing to a type raises error."""
    expect_load_error(
        ErrorCode.TYPE_RESOLVE_ERROR,
        YamlObject,
        'object_field: !type:tests.fixtures.IDontExist\n' +
        '  test_field: test_value\n' +
        '  child_field: child_value\n'
    )

    expect_load_error(
        ErrorCode.TYPE_RESOLVE_ERROR,
        YamlObject,
        'object_field: !type:tests.fixtures.expect_load_error\n' +
        '  test_field: test_value\n' +
        '  child_field: child_value\n'
    )


def test_bad_formatted_type_tag():
    """Test an error is raised for badly formatted type tags."""
    expect_load_error(
        ErrorCode.BAD_TYPE_TAG_FORMAT,
        YamlObject,
        (
            'object_field: !typetests.fixtures.SubObjectChild\n' +
            '  test_field: test_value'
        )
    )

    expect_load_error(
        ErrorCode.BAD_TYPE_TAG_FORMAT,
        YamlObject,
        (
            'object_field: !type:tests:fixtures.SubObjectChild\n' +
            '  test_field: test_value'
        )
    )

    expect_load_error(
        ErrorCode.BAD_TYPE_TAG_FORMAT,
        YamlObject,
        (
            'object_field: !type:tests\n' +
            '  test_field: test_value'
        )
    )
