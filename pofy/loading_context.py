"""Loading context class & utilities."""
from contextlib import contextmanager
from typing import AnyStr
from typing import Callable
from typing import List
from typing import Union

from yaml import MappingNode
from yaml import Node
from yaml import SequenceNode

from .errors import ErrorCode
from .errors import PofyError
from .resolvers import Resolver


class LoadingContext:
    """Context aggregating resolve & error reporting functions."""

    def __init__(
        self,
        error_handler: Callable,
        resolvers: List[Resolver]
    ):
        """Initialize context."""
        self._error_handler = error_handler
        self._resolvers = resolvers
        self._node_stack = []

    @contextmanager
    def push(self, node: Node):
        """Push a node in the context.

        This is solely used to know which node is currently loaded when calling
        error function, to avoid having to pass around node objects.

        Args:
            node: Currently loaded node.

        """
        if len(self._node_stack) > 0:
            assert self._node_stack[-1] != node

        self._node_stack.append(node)
        yield
        self._node_stack.pop()

    def current_node(self):
        """Return the currently loaded node."""
        nodes = self._node_stack
        assert len(nodes) > 0
        return nodes[-1]

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
        assert len(self._node_stack) > 0
        node = self._node_stack[-1]
        message = message_format.format(*args, **kwargs)
        if self._error_handler is not None:
            self._error_handler(node, code, message)
        else:
            raise PofyError(node, code, message)

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
