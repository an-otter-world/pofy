"""List field class & utilities."""
from gettext import gettext as _
from typing import Type

from yaml import MappingNode

from pyyo.errors import parse_error
from pyyo.loader import load

from .base_field import BaseField


class ObjectField(BaseField):
    """Dict YAML object field."""

    def __init__(self, *args, object_class: Type = object, **kwargs):
        """Initialize object field.

        Arg:
            object_class (class) : The class of the object to create.
            *args, **kwargs (list, dict) : Arguments forwarded to BaseField.

        """
        super().__init__(*args, **kwargs)
        self._object_class = object_class

    def deserialize(self, node):
        """See pyyo.BaseField.deserialize for usage."""
        if not isinstance(node, MappingNode):
            parse_error(node, _('Expected a mapping'))

        return load(self._object_class, node)
