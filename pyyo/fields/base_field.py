"""Base field class & utilities."""
from abc import abstractmethod
from gettext import gettext as _
from yaml import Node
from yaml import ScalarNode

from pyyo.errors import parse_error
from pyyo.loading_context import LoadingContext


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

    def load(self, node: Node, context: LoadingContext):
        """Deserialize this field.

        Args:
        ----
            node (yaml.Node) : YAML node containing field value.
            context (LoadingContext) : Resolver used to resolve !include tags.

        Return:
        ------
            (object) : Deserialized field value.

        """
        if node.tag == '!include':
            if not isinstance(node, ScalarNode):
                context.error(node, _('Expected a string after include tag'))
            else:
                location = node.value
                node = context.resolve(location)
        return self._load(node, context)

    @abstractmethod
    def _load(self, node: Node, context: LoadingContext):
        """Deserialize this field using the given node.

        Args:
        ----
            node (yaml.Node) : YAML node containing field value.
            context (LoadingContext): The loading context.

        Return:
        ------
            (object) : Deserialized field value.

        """
        raise NotImplementedError


class ScalarField(BaseField):
    """Base class for scalar value fields."""

    def _load(self, node, context):
        if not isinstance(node, ScalarNode):
            parse_error(node, _('Exected scalar value.'))

        return self._convert(node.value)

    @abstractmethod
    def _convert(self, value: str):
        """Convert the string value to wanted type.

        Args:
        ----
            value (str) : the field value as string

        Return:
        ------
            (any) : The converted value

        """
        raise NotImplementedError
