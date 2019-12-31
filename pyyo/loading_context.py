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

    def __init__(self, resolvers: List[Resolver]):
        """Initialize context."""
        self._resolvers = resolvers
        self._errors = []

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
        self._errors.append(node, message)

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

        assert result is None or isinstance(result, MappingNode, SequenceNode)
        return result
