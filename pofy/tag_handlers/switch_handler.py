"""Handler selecting the first non-failure value in a list."""
from typing import Any
from yaml import SequenceNode

from pofy.common import UNDEFINED
from pofy.interfaces import IBaseField
from pofy.interfaces import ILoadingContext
from pofy.tag_handlers.tag_handler import TagHandler


class SwitchHandler(TagHandler):
    """Tag selecting the first value that is defined in a list."""

    tag_pattern = r'^switch$'

    def load(self, context: ILoadingContext, field: IBaseField) \
            -> Any:
        if not context.expect_sequence():
            return UNDEFINED

        node = context.current_node()
        assert isinstance(node, SequenceNode)

        for child in node.value:
            result = context.load(field, child)
            if result is not UNDEFINED:
                return result

        return UNDEFINED
