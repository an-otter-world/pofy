"""Test fixtures & dummy classes."""
from typing import AnyStr
from typing import IO
from typing import List
from typing import Type
from typing import Union

from yaml import Node

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


def _validate(node: Node, context: LoadingContext, _: str):
    context.error(node, ErrorCode.VALIDATION_ERROR, 'Test')
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
