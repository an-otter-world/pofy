"""Loading context class & utilities."""
from contextlib import contextmanager
from gettext import gettext as _
from typing import AnyStr
from typing import Callable
from typing import List
from typing import Type

from yaml import MappingNode
from yaml import Node
from yaml import ScalarNode
from yaml import SequenceNode

from .errors import ErrorCode
from .errors import PofyError
from .tag_handlers.tag_handler import TagHandler


class LoadingContext:
    """Context aggregating resolve & error reporting functions."""

    def __init__(
        self,
        error_handler: Callable,
        tag_handlers: List[TagHandler]
    ):
        """Initialize context."""
        self._error_handler = error_handler
        self._tag_handlers = tag_handlers
        self._node_stack = []

    @contextmanager
    def load(self, node: Node):
        """Push a node in the context.

        This is solely used to know which node is currently loaded when calling
        error function, to avoid having to pass around node objects.

        Args:
            node: Currently loaded node.

        """
        if len(self._node_stack) > 0:
            assert self._node_stack[-1] != node

        # The node returned by handle_tag can be different than the one passed
        # as argument (for example, the given node is an !import node)

        self._node_stack.append(node)

        transformed_node = self._handle_tag(node)

        if transformed_node is None:
            yield False
        elif transformed_node == node:
            yield True
        else:
            with self.load(transformed_node) as loaded:
                yield loaded

        self._node_stack.pop()

    def current_node(self):
        """Return the currently loaded node."""
        nodes = self._node_stack
        assert len(nodes) > 0
        return nodes[-1]

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
        node = self._node_stack[-1]
        message = message_format.format(*args, **kwargs)
        if self._error_handler is not None:
            self._error_handler(node, code, message)
        else:
            raise PofyError(node, code, message)

    def _expect_node(
        self,
        node_type: Type[Node],
        error_format: AnyStr,
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

    def _handle_tag(self, node):
        tag = node.tag
        if not tag.startswith('!'):
            return node

        transformed_node = None
        handler_found = False
        for handler in self._tag_handlers:
            if not handler.match(node):
                continue

            handler_found = True

            if transformed_node is not None:
                self.error(
                    ErrorCode.MULTIPLE_MATCHING_HANDLERS,
                    _('Got multiple matching handlers for tag {}'), tag
                )
                continue

            transformed_node = handler.transform(self)

        if not handler_found:
            return node

        return transformed_node
