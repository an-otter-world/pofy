"""Base deserialilable YAML object class & utilities."""
from gettext import gettext as _
from inspect import getmembers
from io import StringIO
from yaml import MappingEndEvent
from yaml import MappingStartEvent
from yaml import parse

from .base_field import BaseField
from .parse_error import parse_error

class YamlObject:
    """Base class for YAML deserializable object."""

    def __init__(self, source):
        """Initialize YamlObject.

        Args:
            source (str, stream) : Either a string or a stream to parse to
                                   construct this object.
        """
        if isinstance(source, str):
            source = StringIO(source)

        self._load(source)

    def _load(self, source):
        fields = dict(self._get_fields())
        events = iter(parse(source))

        while not isinstance(next(events), MappingStartEvent):
            pass

        event = next(events)
        while not isinstance(event, MappingEndEvent):
            field_name = event.value
            if not field_name in fields:
                parse_error(event, _('Unknown field {}'), field_name)
            field = fields[field_name]
            field_value = field.deserialize(events)
            setattr(self, field_name, field_value)
            event = next(events)

    @classmethod
    def _get_fields(cls):
        def _is_field(member):
            return isinstance(member, BaseField)

        for name, field in getmembers(cls, _is_field):
            yield (name, field)
