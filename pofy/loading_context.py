"""Loading context class & utilities."""
from gettext import gettext as _
from typing import Any
from typing import Callable
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type

from yaml import MappingNode
from yaml import Node
from yaml import ScalarNode
from yaml import SequenceNode

from pofy.errors import ErrorCode
from pofy.errors import get_exception_type
from pofy.common import ILoadingContext
from pofy.common import IBaseField
from pofy.tag_handlers.tag_handler import TagHandler

ErrorHandler = Optional[Callable[[Node, ErrorCode, str], Any]]
NodeStack = List[Tuple[Node, Optional[str]]]


class LoadingContext(ILoadingContext):
    """Context aggregating resolve & error reporting functions."""

    def __init__(
        self,
        error_handler: ErrorHandler,
        tag_handlers: List[TagHandler]
    ):
        """Initialize context."""
        self._error_handler = error_handler
        self._tag_handlers = tag_handlers
        self._node_stack: NodeStack = []

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
        if len(self._node_stack) > 0:
            assert self._node_stack[-1] != node

        self._node_stack.append((node, location))

        try:
            tag_handler = self._get_tag_handler(node)
            if tag_handler is not None:
                result = tag_handler.load(self, field)
            else:
                result = field.load(self)
        finally:
            self._node_stack.pop()

        return result

    def current_node(self) -> Node:
        """Return the currently loaded node."""
        nodes = self._node_stack
        assert len(nodes) > 0
        return nodes[-1][0]

    def current_location(self) -> Optional[str]:
        """Return the location of the document owning the current node.

        If no path can be found, returs None.
        """
        for __, location in reversed(self._node_stack):
            if location is not None:
                return location

        return None

    def expect_scalar(self, message: str = None):
        """Return false and raise an error if the current node isn't scalar."""
        if message is None:
            message = _('Expected a scalar value.')
        return self._expect_node(
            ScalarNode,
            message
        )

    def expect_sequence(self):
        """Return false and raise if the current node isn't a sequence."""
        return self._expect_node(
            SequenceNode,
            _('Expected a sequence value.')
        )

    def expect_mapping(self):
        """Return false and raise if the current node isn't a mapping."""
        return self._expect_node(
            MappingNode,
            _('Expected a mapping value.')
        )

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
        node, __ = self._node_stack[-1]
        message = message_format.format(*args, **kwargs)
        if self._error_handler is not None:
            self._error_handler(node, code, message)
        else:
            exception_type = get_exception_type(code)
            raise exception_type(node, message)

    def _expect_node(
        self,
        node_type: Type[Node],
        error_format: str,
        *args,
        **kwargs
    ):
        current_node = self.current_node()
        if not isinstance(current_node, node_type):
            self.error(
                ErrorCode.UNEXPECTED_NODE_TYPE,
                error_format,
                *args,
                **kwargs
            )
            return False

        return True

    def _get_tag_handler(self, node: Node) -> Optional[TagHandler]:
        tag = node.tag
        if not tag.startswith('!'):
            return None

        found_handler = None
        for handler in self._tag_handlers:
            if not handler.match(node):
                continue

            if found_handler is not None:
                self.error(
                    ErrorCode.MULTIPLE_MATCHING_HANDLERS,
                    _('Got multiple matching handlers for tag {}'), tag
                )
                continue

            found_handler = handler

        return found_handler
