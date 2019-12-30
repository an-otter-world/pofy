"""List field class & utilities."""
from gettext import gettext as _

from yaml import MappingNode

from pyyo.errors import parse_error

from .base_field import BaseField

class ObjectField(BaseField):
    """Dict YAML object field."""

    def __init__(self, object_class=object):
        """Initialize object field.

        Arg:
            object_class (class) : The class of the object to create.
        """
        self._object_class = object_class

    def deserialize(self, node):
        """See pyyo.BaseField.deserialize for usage."""
        if not isinstance(node, MappingNode):
            parse_error(node, _('Expected a mapping'))

        from pyyo.deserializer import deserialize
        return deserialize(node, self._object_class)
