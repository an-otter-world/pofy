"""Object field tests."""
from pofy import ErrorCode
from pofy import ObjectField
from pofy import StringField
from pofy import load

from tests.fixtures import expect_load_error
from tests.fixtures import load_with_fail_tag


class _SubObject:

    class Schema:
        """Pofy fields."""

        test_field = StringField()


class _SubObjectChild(_SubObject):

    class Schema:
        """Pofy fields."""

        child_field = StringField()


class _SubObjectOwner:

    class Schema:
        """Pofy fields."""

        object_field = ObjectField(object_class=_SubObject)


def test_object_field():
    """Test object field loading works."""
    test = load(
        'object_field:\n'
        '  test_field: field_value\n',
        _SubObjectOwner,
    )
    assert isinstance(test.object_field, _SubObject)
    assert test.object_field.test_field == 'field_value'


def test_object_field_error_on_bad_node():
    """Test object field loading raises an error on bad node."""
    expect_load_error(
        ErrorCode.UNEXPECTED_NODE_TYPE,
        'object_field:\n'
        '  - item1\n'
        '  - item2',
        _SubObjectOwner,
    )


def test_type_tag():
    """Test specifying a type for an object field works."""
    test = load(
        'object_field: !type:tests.fields.test_object_field._SubObjectChild\n'
        '  test_field: test_value\n'
        '  child_field: child_value\n',
        _SubObjectOwner,
    )
    assert isinstance(test.object_field, _SubObjectChild)
    assert test.object_field.test_field == 'test_value'
    assert test.object_field.child_field == 'child_value'


def test_bad_type_raise_error():
    """Test a type tag not existing or not pointing to a type raises error."""
    expect_load_error(
        ErrorCode.TYPE_RESOLVE_ERROR,
        'object_field: !type:tests.fixtures.IDontExist\n'
        '  test_field: test_value\n'
        '  child_field: child_value\n',
        _SubObjectOwner,
    )

    expect_load_error(
        ErrorCode.TYPE_RESOLVE_ERROR,
        'object_field: !type:tests.fixtures.expect_load_error\n'
        '  test_field: test_value\n'
        '  child_field: child_value\n',
        _SubObjectOwner,
    )


def test_bad_formatted_type_tag():
    """Test an error is raised for badly formatted type tags."""
    expect_load_error(
        ErrorCode.BAD_TYPE_TAG_FORMAT,
        'object_field: !typetests.fixtures.SubObjectChild\n'
        '  test_field: test_value',
        _SubObjectOwner,
    )

    expect_load_error(
        ErrorCode.BAD_TYPE_TAG_FORMAT,
        'object_field: !type:tests:fixtures.SubObjectChild\n'
        '  test_field: test_value',
        _SubObjectOwner,
    )

    expect_load_error(
        ErrorCode.BAD_TYPE_TAG_FORMAT,
        'object_field: !type:tests\n'
        '  test_field: test_value',
        _SubObjectOwner,
    )


def test_object_field_load_subclass():
    """Test fields declared in parent classes are loaded."""
    class _Parent:
        class Schema:
            """Pyfo fields."""

            parent_field = StringField()

    class _Child(_Parent):
        class Schema:
            """Pyfo fields."""

            child_field = StringField()

    test = load(
        'parent_field: parent_value\n'
        'child_field: child_value',
        _Child,
    )

    assert test.parent_field == 'parent_value'
    assert test.child_field == 'child_value'


def test_object_validation_works():
    """Test object validation methods are executed."""

    class _ValidatedObject:
        class Schema:
            """Pofy fields."""

            dont_set_me = StringField()

            @classmethod
            def validate(cls, context, obj):
                """Validate loaded objects."""
                if obj.dont_set_me is not None:
                    context.error(ErrorCode.VALIDATION_ERROR, 'Error')
                return False

        def __init__(self):
            """Initialize."""
            self.dont_set_me = None

    class _ValidatedObjectChild(_ValidatedObject):
        class Schema:
            """Pofy fields."""

            @classmethod
            def validate(cls, __, ___):
                """Validate loaded objects."""
                return True

    expect_load_error(
        ErrorCode.VALIDATION_ERROR,
        'dont_set_me: Wathever',
        _ValidatedObjectChild,
    )


def test_unknown_field_raise_error():
    """Test an undeclared field in YAML raises an error."""
    class _EmptyObject:
        class Schema:
            """Pyfo fields."""

    expect_load_error(
        ErrorCode.FIELD_NOT_DECLARED,
        'uknown_field: 10',
        _EmptyObject,
    )


def test_unset_required_field_raise_error():
    """Test an unset required field in YAML raise an error."""
    class _RequiredFieldObject:
        class Schema:
            """Pofy fields."""

            required = StringField(required=True)
            not_required = StringField()

    expect_load_error(
        ErrorCode.MISSING_REQUIRED_FIELD,
        'not_required: some_value',
        _RequiredFieldObject,
    )

    test = load(
        'required: setted\n'
        'not_required: yodeldi',
        _RequiredFieldObject,
    )
    assert test.required == 'setted'
    assert test.not_required == 'yodeldi'


def test_object_field_ignores_tag_handler_failure():
    """Test that object field just doesn't add fields when tag handler fails."""
    class _TestObject:
        class Schema:
            """Pyfo fields."""

            field_1 = StringField()
            field_2 = StringField()
            field_3 = StringField()

    test = load_with_fail_tag(
        'field_1: !fail test_value\n'
        '!fail field_2: test_value\n'
        'field_3: test_value\n',
        _TestObject,
    )

    assert not hasattr(test, 'field_1')
    assert not hasattr(test, 'field_2')
    assert test.field_3 == 'test_value'


def test_object_without_schema_raise_error():
    """Test giving a type without a Schema raise an an error."""
    class _ObjectWithoutSchema:
        pass

    expect_load_error(
        ErrorCode.SCHEMA_ERROR,
        'i_should: not_event_be_parsed',
        _ObjectWithoutSchema,
    )


def test_post_load_called():
    """Test that post_load methods are called."""
    post_load_called = False

    class _PostLoadObject:
        class Schema:
            """Pofy fields."""

            test_field = StringField()

            @classmethod
            def post_load(cls, obj):
                """Post load."""

                nonlocal post_load_called
                post_load_called = True
                assert obj.test_field == 'test_value'

    load('test_field: test_value', _PostLoadObject)
    assert post_load_called
