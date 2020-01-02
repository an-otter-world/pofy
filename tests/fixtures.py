"""Test fixtures & dummy classes."""
from typing import AnyStr
from typing import IO
from typing import List
from typing import Type
from typing import Union

from pofy import BoolField
from pofy import DictField
from pofy import ErrorCode
from pofy import FloatField
from pofy import IntField
from pofy import ListField
from pofy import LoadingContext
from pofy import ObjectField
from pofy import Resolver
from pofy import StringField
from pofy import load


class SubObject:
    """Test class for object field of YamlObject."""

    class Schema:
        """Pofy fields."""

        test_field = StringField()


class SubObjectChild(SubObject):
    """Test class for object field of YamlObject, subclassing another class."""

    class Schema:
        """Pofy fields."""

        child_field = StringField()


def _validate(context: LoadingContext, _: str):
    context.error(ErrorCode.VALIDATION_ERROR, 'Test')
    return False


class YamlObject:
    """Test class for serialization tests."""

    class Schema:
        """Pofy fields."""

        bool_field = BoolField()
        dict_field = DictField(StringField())
        float_field = FloatField()
        int_field = IntField()
        hex_int_field = IntField(base=16)
        list_field = ListField(StringField())
        object_field = ObjectField(object_class=SubObject)
        object_list_field = ListField(ObjectField(object_class=SubObject))
        string_field = StringField()
        validated_field = StringField(validate=_validate)
        bounded_int_field = IntField(minimum=10, maximum=20)
        bounded_float_field = FloatField(minimum=10.0, maximum=20.0)

    def __init__(self):
        """Initialize YamlObject."""
        self.dict_field = {}
        self.int_field = 0
        self.list_field = []
        self.object_field = None
        self.string_field = ''
        self.object_list_field = []


class RequiredFieldObject:
    """Stub with a required field."""

    class Schema:
        """Pofy fields."""

        required = StringField(required=True)
        not_required = StringField(required=True)


class ValidatedObject:
    """Object with a validation method."""

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


class ValidatedObjectChild(ValidatedObject):
    """Stub to check parent validation methods are called."""

    class Schema:
        """Pofy fields."""

        @classmethod
        def validate(cls, __, ___):
            """Validate loaded objects."""
            return True

    def __init__(self):
        """Initialize."""
        super().__init__()
        self.dont_set_me = None


def expect_load_error(
    expected_error: ErrorCode,
    object_class: Type,
    source: Union[AnyStr, IO[str]],
    resolvers: List[Resolver] = None
):
    """Load the given object, expecting an error to be raised."""
    error_raised = False

    def _on_error(__, error, ___):
        nonlocal error_raised
        error_raised = True
        assert error == expected_error

    load(
        object_class,
        source,
        error_handler=_on_error,
        resolvers=resolvers
    )
