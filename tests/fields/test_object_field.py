"""Object field tests."""
from typing import Any
from typing import Optional

from pofy.common import ErrorCode
from pofy.common import UNDEFINED
from pofy.fields.bool_field import BoolField
from pofy.fields.object_field import ObjectField
from pofy.fields.string_field import StringField
from pofy.interfaces import ILoadingContext

from tests.helpers import check_field_error
from tests.helpers import check_load


class _Owned:

    class Schema:
        """Pofy fields."""

        required_field = StringField(required=True)
        error = BoolField()

        @classmethod
        def validate(cls, context: ILoadingContext, obj: Any) -> bool:
            """Validate."""
            if getattr(obj, 'error', False):
                context.error(ErrorCode.VALIDATION_ERROR, 'Error')
                return False
            obj.parent_validate_called = True
            return True

        @classmethod
        def post_load(cls, obj: Any) -> None:
            """Postload."""
            obj.parent_post_load_called = True

    def __init__(self) -> None:
        """Initialize object."""
        self.required_field: Optional[str] = None
        self.parent_validate_called = False
        self.parent_post_load_called = False


class _OwnedChild(_Owned):

    class Schema:
        """Pofy fields."""

        child_field = StringField()

        @classmethod
        def validate(cls, _: ILoadingContext, obj: Any) -> bool:
            """Validate."""
            obj.child_validate_called = True
            return True

        @classmethod
        def post_load(cls, obj: Any) -> None:
            """Postload."""
            obj.child_post_load_called = True

    def __init__(self) -> None:
        """Initialize object."""
        super().__init__()
        self.child_field: Optional[str] = None
        self.child_validate_called = False
        self.child_post_load_called = False


class _Owner:

    class Schema:
        """Pofy fields."""

        field = ObjectField(object_class=_Owned)

        @classmethod
        def validate(cls, __: ILoadingContext, obj: Any) -> bool:
            """Validate loaded objects."""
            obj.validate_called = True
            return True

        @classmethod
        def post_load(cls, obj: Any) -> None:
            """Post load."""
            obj.post_load_called = True

    def __init__(self) -> None:
        """Initialize _Owner."""
        self.field: Optional[_Owned] = None


class _ValidationError:
    class Schema:
        """Pofy fields."""

        @classmethod
        def validate(cls, context: ILoadingContext, __: Any) -> bool:
            """Validate loaded objects."""
            context.error(ErrorCode.VALIDATION_ERROR, 'Error')
            return False


class _NoSchema:
    pass


class _Simple:
    class Schema:
        """Pofy fields."""

        field = StringField()


def _check_field_error(yaml_value: str, expected_error: ErrorCode) -> None:
    check_field_error(_Owner, 'field', yaml_value, expected_error)


def test_object_field() -> None:
    """Object field should load correct values."""
    result = check_load(
        'field: !type:tests.fields.test_object_field._OwnedChild\n'
        '  required_field: parent_value\n'
        '  child_field: child_value\n',
        _Owner,
    )
    assert isinstance(result, _Owner)
    assert isinstance(result.field, _OwnedChild)
    assert result.field.required_field == 'parent_value'
    assert result.field.child_field == 'child_value'
    assert result.field.parent_validate_called
    assert result.field.parent_post_load_called
    assert result.field.child_validate_called
    assert result.field.child_post_load_called

    result = check_load('field: value\n', _Simple)
    assert hasattr(result, 'field')
    assert result.field == 'value'

    result = check_load('field: !fail value\n', _Simple)
    assert not hasattr(result, 'field')

    result = check_load('!fail field: value\n', _Simple)
    assert not hasattr(result, 'field')


def test_object_field_error_handling() -> None:
    """Object field should correctly handle errors."""
    _check_field_error('scalar_value', ErrorCode.UNEXPECTED_NODE_TYPE)
    _check_field_error('[a, list]', ErrorCode.UNEXPECTED_NODE_TYPE)

    _check_field_error('!type:dont.Exists {}', ErrorCode.TYPE_RESOLVE_ERROR)
    _check_field_error('!type:os.not_a_module {}', ErrorCode.TYPE_RESOLVE_ERROR)
    # Not a class
    _check_field_error('!type:os.abort {}', ErrorCode.TYPE_RESOLVE_ERROR)

    _check_field_error('!typebad.Format {}', ErrorCode.BAD_TYPE_TAG_FORMAT)
    _check_field_error('!type:bad:Format {}', ErrorCode.BAD_TYPE_TAG_FORMAT)
    _check_field_error('!type:bad {}', ErrorCode.BAD_TYPE_TAG_FORMAT)

    _check_field_error(
        '{ required_field: value, unknown_field: value }',
        ErrorCode.FIELD_NOT_DECLARED
    )

    _check_field_error(
        '{ required_field: value, error: On }',
        ErrorCode.VALIDATION_ERROR
    )

    _check_field_error('{ }', ErrorCode.MISSING_REQUIRED_FIELD)

    obj = check_load('{ }', _NoSchema, ErrorCode.SCHEMA_ERROR)
    assert obj == UNDEFINED
