"""Handler loading a value only if some flag is defined."""
from typing import Any
from typing import Optional
from yaml import MappingNode
from yaml import Node
from yaml import ScalarNode
from yaml import SequenceNode

from pofy.common import LOADING_FAILED
from pofy.interfaces import IBaseField
from pofy.interfaces import ILoadingContext
from pofy.tag_handlers.tag_handler import TagHandler


class IfHandler(TagHandler):
    """Tag loading a value only if some flag is defined on loading.

    See pofy.load method to set flags.
    """

    tag_pattern = r'^if\((?P<flag>[\w|_]*)\)$'

    def load(self, context: ILoadingContext, field: IBaseField) \
            -> Any:
        node = context.current_node()
        tag = node.tag[1:] # Remove trailing !
        match = self._compiled_pattern.match(tag)

        # The pattern should match already if we're here
        assert match is not None

        flag = match.group('flag')

        if not context.is_defined(flag):
            return LOADING_FAILED

        # We need to return a copy of the node to avoid infinite recursion
        # that would happen if we return a node with an if tag defined on it
        node_copy: Optional[Node] = None

        if isinstance(node, ScalarNode):
            node_copy = ScalarNode(
                tag='',
                value=node.value,
                start_mark=node.start_mark,
                end_mark=node.end_mark,
                style=node.style
            )
        elif isinstance(node, SequenceNode):
            node_copy = SequenceNode(
                tag='',
                value=node.value,
                start_mark=node.start_mark,
                end_mark=node.end_mark,
                flow_style=node.flow_style
            )
        elif isinstance(node, MappingNode):
            node_copy = MappingNode(
                tag='',
                value=node.value,
                start_mark=node.start_mark,
                end_mark=node.end_mark,
                flow_style=node.flow_style
            )

        assert node_copy is not None, "Unkown node type"
        return context.load(field, node_copy)
