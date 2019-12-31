"""Test fixtures & dummy classes."""
from pyyo import DictField
from pyyo import IntField
from pyyo import ListField
from pyyo import ObjectField
from pyyo import StringField


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

    def __init__(self):
        """Initialize YamlObject."""
        self.dict_field = {}
        self.int_field = 0
        self.list_field = []
        self.object_field = None
        self.string_field = ''


class RequiredFieldObject:
    """Stub with a required field."""

    class Schema:
        """Pyyo fields."""

        required = StringField(required=True)
        not_required = StringField(required=True)
