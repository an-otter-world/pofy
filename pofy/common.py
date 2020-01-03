"""Pofy common definitions."""
from abc import abstractmethod
from typing import Any
from typing import Optional

from yaml import Node

from pofy.errors import ErrorCode

# Unique symbol used to differentiate an error from a valid None return when
# loading a field.
LOADING_FAILED = object()


class IBaseField:
    """Interface used to avoid cyclic imports for type hint."""

    @abstractmethod
    def load(self, context: 'ILoadingContext') -> Any:
        """Deserialize this field.

        Args:
            node: YAML node containing field value.
            context: Loading context, handling include resolving and error
                     management.

        Return:
            Deserialized field value, or LOADING_FAILED if loading failed.

        """


class ILoadingContext:
    """Interface used to avoid cyclic imports for type hint."""

    @abstractmethod
    def load(
        self,
        field: IBaseField,
        node: Node,
        location: Optional[str] = None
    ) -> Any:
        """Push a node in the context.

        This is solely used to know which node is currently loaded when calling
        error function, to avoid having to pass around node objects.

        Args:
            field: Field describing this node.
            node: Currently loaded node.
            location: The path from which this node was loaded. Every node
                       pushed subsequently will be considered having the
                       same path, except until another child path is pushed.

        """

    @abstractmethod
    def current_node(self) -> Node:
        """Return the currently loaded node."""

    @abstractmethod
    def current_location(self) -> Optional[str]:
        """Return the location of the document owning the current node.

        If no path can be found, returs None.
        """

    @abstractmethod
    def expect_scalar(self, message: str = None):
        """Return false and raise an error if the current node isn't scalar."""

    @abstractmethod
    def expect_sequence(self):
        """Return false and raise if the current node isn't a sequence."""

    @abstractmethod
    def expect_mapping(self):
        """Return false and raise if the current node isn't a mapping."""

    @abstractmethod
    def error(
        self,
        code: ErrorCode,
        message_format: str,
        *args,
        **kwargs
    ):
        """Register an error in the current loading context.

        If errors occured in the scope of a context, an error will be raised
        at the end of the object loading.

        Args:
            code: Code of the error.
            message_format: The error message format.
            *args, **kwargs: Arguments used to format message.

        """