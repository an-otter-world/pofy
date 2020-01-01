"""Base field class & utilities."""
from abc import abstractmethod
from gettext import gettext as _
from typing import Any

from yaml import Node
from yaml import ScalarNode

from pyyo.errors import ErrorCode
from pyyo.loading_context import LoadingContext


class BaseField:
    """Base class for YAML object fields."""

    def __init__(self, required: bool = False):
        """Initialize the field.

        Args:
            required: If it's true and the field is not defined in yaml, it
                      will create an error that will eventually be raised at
                      the end of deserialization.

        """
        self.required = required

    def load(self, node: Node, context: LoadingContext) -> Any:
        """Deserialize this field.

        Args:
            node: YAML node containing field value.
            context: Loading context, handling include resolving and error
                     management.

        Return:
            Deserialized field value.

        """
        if node.tag == '!include':
            if not isinstance(node, ScalarNode):
                context.error(
                    node,
                    ErrorCode.UNEXPECTED_NODE_TYPE,
                    _('!include tag must be on a scalar node')
                )
                return None

            location = node.value
            node = context.resolve(location)
            if node is None:
                context.error(
                    node,
                    ErrorCode.INCLUDE_NOT_FOUND,
                    _("Can't resolve include {}"), location
                )
                return None

        return self._load(node, context)

    @abstractmethod
    def _load(self, node: Node, context: LoadingContext) -> Any:
        """Deserialize this field using the given node.

        Args:
            node: YAML node containing field value.
            context: Loading context, handling include resolving and error
                     management.

        Return:
            Deserialized field value.

        """
        raise NotImplementedError


class ScalarField(BaseField):
    """Base class for scalar value fields."""

    def _load(self, node, context):
        if not isinstance(node, ScalarNode):
            context.error(
                node,
                ErrorCode.UNEXPECTED_NODE_TYPE,
                _('Scalar expected')
            )
            return None

        return self._convert(node.value)

    @abstractmethod
    def _convert(self, value: str) -> Any:
        """Convert the string value to the target type of this field.

        Args:
            value : the field value as string.

        Return:
            The converted value.

        """
        raise NotImplementedError
