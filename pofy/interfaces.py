"""Pofy common definitions."""
from abc import abstractmethod
from typing import Any
from typing import Optional

from yaml import Node

from pofy.common import ErrorCode
from pofy.common import SchemaResolver


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
            Deserialized field value, or UNDEFINED if loading failed.

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
    def is_defined(self, flag: str) -> bool:
        """Return true if the given flag was defined when calling load."""

    @abstractmethod
    def get_schema_resolver(self) -> SchemaResolver:
        """Return a function returning the schema for the given type."""

    @abstractmethod
    def current_node(self) -> Node:
        """Return the currently loaded node."""

    @abstractmethod
    def current_location(self) -> Optional[str]:
        """Return the location of the document owning the current node.

        If no path can be found, returs None.
        """

    @abstractmethod
    def expect_scalar(self, message: Optional[str] = None) -> bool:
        """Return false and raise an error if the current node isn't scalar."""

    @abstractmethod
    def expect_sequence(self) -> bool:
        """Return false and raise if the current node isn't a sequence."""

    @abstractmethod
    def expect_mapping(self) -> bool:
        """Return false and raise if the current node isn't a mapping."""

    @abstractmethod
    def error(
        self,
        code: ErrorCode,
        message_format: str,
        *args: Any,
        **kwargs: Any
    ) -> None:
        """Register an error in the current loading context.

        If errors occured in the scope of a context, an error will be raised
        at the end of the object loading.

        Args:
            code: Code of the error.
            message_format: The error message format.
            *args, **kwargs: Arguments used to format message.

        """
