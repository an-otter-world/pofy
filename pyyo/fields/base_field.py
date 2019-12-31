"""Base field class & utilities."""
from abc import abstractmethod
from gettext import gettext as _
from yaml import Node
from yaml import ScalarNode

from pyyo.errors import parse_error


class BaseField:
    """Base class for YAML object fields."""

    def __init__(self, required=False):
        """Initialize the field.

        Args:
        ----
            required (bool) : If it's true and the field is not defined in
                              yaml, a ParseError will be raised when
                              parsing.

        """
        self.required = required

    @abstractmethod
    def deserialize(self, node: Node):
        """Deserialize this field.

        Args:
        ----
            node (yaml.Node) : YAML node containing field value.

        Return:
        ------
            (object) : Deserialized field value.

        """
        raise NotImplementedError


class ScalarField(BaseField):
    """Base class for scalar value fields."""

    def deserialize(self, node):
        """See BaseField.deserialize method documentation."""
        if not isinstance(node, ScalarNode):
            parse_error(node, _('Exected scalar value.'))

        return self._convert(node.value)

    @abstractmethod
    def _convert(self, value):
        """Convert the string value to wanted type.

        Args:
        ----
            value (str) : the field value as string

        Return:
        ------
            (any) : The converted value

        """
        raise NotImplementedError
