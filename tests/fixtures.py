"""Test fixtures & dummy classes."""
from typing import AnyStr
from typing import IO
from typing import List
from typing import Type
from typing import Union

from pyyo import DictField
from pyyo import ErrorCode
from pyyo import IntField
from pyyo import ListField
from pyyo import ObjectField
from pyyo import Resolver
from pyyo import StringField
from pyyo import load


class SubObject:
    """Test class for object field of YamlObject."""

    class Schema:
        """Pyyo fields."""

        test_field = StringField()


class SubObjectChild(SubObject):
    """Test class for object field of YamlObject, subclassing another class."""

    class Schema:
        """Pyyo fields."""

        child_field = StringField()


class YamlObject:
    """Test class for serialization tests."""

    class Schema:
        """Pyyo fields."""

        dict_field = DictField(StringField())
        int_field = IntField()
        list_field = ListField(StringField())
        object_field = ObjectField(object_class=SubObject)
        string_field = StringField()
        object_list_field = ListField(ObjectField(object_class=SubObject))

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
        """Pyyo fields."""

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
