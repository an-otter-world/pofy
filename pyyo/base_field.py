"""Base field class & utilities."""
from abc import abstractmethod
from gettext import gettext as _
from yaml import ScalarEvent

from .parse_error import parse_error

class BaseField:
    """Base class for YAML object fields."""

    @abstractmethod
    def deserialize(self, events):
        """Deserialize this field.

        Args:
            events (iterator) : YAML events iterator.

        Return:
            (object) : Deserialized field value.
        """
        raise NotImplementedError

class ScalarField(BaseField):
    """Base class for scalar value fields."""

    def deserialize(self, events):
        """See BaseField.deserialize method documentation."""
        event = next(events)
        if not isinstance(event, ScalarEvent):
            parse_error(event, _('Exected scalar value.'))

        return self._convert(event.value)

    @abstractmethod
    def _convert(self, value):
        """Convert the string value to wanted type.

        Arg:
            value (str) : the field value as string

        Return:
            (any) : The converted value
        """
        raise NotImplementedError
