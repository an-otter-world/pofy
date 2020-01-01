"""Object field tests."""
from pyyo import load
from pyyo import ErrorCode

from .fixtures import SubObject
from .fixtures import SubObjectChild
from .fixtures import YamlObject
from .fixtures import expect_load_error


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
