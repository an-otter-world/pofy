"""Loading context class & utilities."""
from typing import AnyStr
from typing import Callable
from typing import List
from typing import Union

from yaml import MappingNode
from yaml import Node
from yaml import SequenceNode

from .errors import ErrorCode
from .errors import PyyoError
from .resolvers import Resolver


class LoadingContext:
    """Context aggregating resolve & error reporting functions."""

    def __init__(
        self,
        error_handler: Callable,
        raise_on_error: bool,
        resolvers: List[Resolver]
    ):
        """Initialize context."""
        self._error_handler = error_handler
        self._errors = []
        self._raise_on_error = raise_on_error
        self._resolvers = resolvers

    def error(
        self,
        node: Node,
        code: ErrorCode,
        message_format: str,
        *args,
        **kwargs
    ):
        """Register an error in the current loading context.

        If errors occured in the scope of a context, an error will be raised
        at the end of the object loading.

        Args:
            node: The node on which the error occured.
            code: Code of the error.
            message_format: The error message format.
            *args, **kwargs: Arguments used to format message.

        """
        message = message_format.format(*args, **kwargs)
        if self._error_handler is not None:
            self._error_handler(node, message)

        if self._raise_on_error:
            raise PyyoError(node, code, message)

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
