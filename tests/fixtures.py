"""Test fixtures & dummy classes."""
from pyyo import DictField
from pyyo import IntField
from pyyo import ListField
from pyyo import ObjectField
from pyyo import StringField


class TestSubObject:
    """Test class for object field of TestObject."""

    class Meta:
        """Pyyo fields."""

        test_field = StringField()


class TestSubObjectChild(TestSubObject):
    """Test class for object field of TestObject, subclassing another class."""

    class Meta:
        """Pyyo fields."""

        child_field = StringField()


class TestObject:
    """Test class for serialization tests."""

    class Meta:
        """Pyyo fields."""

        dict_field = DictField(StringField())
        int_field = IntField()
        list_field = ListField(StringField())
        object_field = ObjectField(TestSubObject)
        string_field = StringField()

    def __init__(self):
        """Initialize TestObject."""
        self.dict_field = {}
        self.int_field = 0
        self.list_field = []
        self.object_field = None
        self.string_field = ''
