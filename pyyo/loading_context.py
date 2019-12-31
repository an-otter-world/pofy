"""Loading context class & utilities."""
from typing import AnyStr
from typing import List
from typing import Union

from yaml import MappingNode
from yaml import Node
from yaml import SequenceNode

from .resolvers import Resolver


class LoadingContext:
    """Context aggregating resolve & error reporting functions."""

    def __init__(self, raise_on_error: bool, resolvers: List[Resolver]):
        """Initialize context."""
        self._raise_on_error = raise_on_error
        self._resolvers = resolvers
        self._errors = []

    def __enter__(self):
        """Enters the context."""
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """Raise an exception if an error occurred during deserialization."""
        if exception_type is not None:
            return False

        if self._raise_on_error and len(self._errors) != 0:
            raise PyyoError(self._errors)

        return False

    def error(self, node: Node, message_format: str, *args, **kwargs):
        """Register an error in the current loading context.

        If errors occured in the scope of a context, an error will be raised
        at the end of the object loading.

        Args:
            node : The node on which the error occured.
            message_format : The error message format.
            *args, **kwargs : Arguments used to format message.

        """
        message = message_format.format(*args, **kwargs)
        self._errors.append((node, message))

    def resolve(self, location: AnyStr) -> Union[MappingNode, SequenceNode]:
        """Resolve given location using registered resolvers.

        Args:
            location : The yaml document to resolve.

        """
        result = None
        for resolver in self._resolvers:
            result = resolver.resolve(location)
            if result is not None:
                break

        assert (
            result is None or
            isinstance(result, (MappingNode, SequenceNode))
        )
        return result


class PyyoError(Exception):
    """Exception raised when errors occurs during object loading."""

    def __init__(self, errors):
        """Initialize the error.

        Arg:
            node : The node on which the error occured.
            message : The error description message.

        """
        super().__init__()
        self.errors = errors
