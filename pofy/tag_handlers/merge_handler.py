"""Handler merging."""
from gettext import gettext as _
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from pofy.common import ErrorCode
from pofy.common import UNDEFINED
from pofy.interfaces import IBaseField
from pofy.interfaces import ILoadingContext
from pofy.tag_handlers.tag_handler import TagHandler


class MergeHandler(TagHandler):
    """Tag merging multiple list or dictionaries into one."""

    tag_pattern = r'^merge$'

    def load(self, context: ILoadingContext, field: IBaseField) \
            -> Any:
        if not context.expect_sequence():
            return UNDEFINED

        node = context.current_node()

        result: Optional[Union[Dict[str, Any], List[Any]]] = None
        for child in node.value:
            child_result = context.load(field, child)
            if child_result is UNDEFINED:
                continue

            if isinstance(child_result, dict):
                if result is None:
                    result = {}

                assert isinstance(result, dict)
                result.update(child_result)

            elif isinstance(child_result, list):
                if result is None:
                    result = []

                assert isinstance(result, list)
                result += child_result

            else:
                msg = _('Trying to merge invalid object {}, expected dict or '
                        'list')
                context.error(ErrorCode.VALUE_ERROR, msg, result)

        # If nothing it's to merge, return UNDEFINED
        if result is None:
            return UNDEFINED

        return result
