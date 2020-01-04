"""Tag handler used to import files in YAML documents."""
from gettext import gettext as _
from typing import Any
from yaml import SequenceNode

from pofy.common import LOADING_FAILED
from pofy.interfaces import ILoadingContext
from pofy.interfaces import IBaseField
from pofy.tag_handlers.path_handler import PathHandler


class GlobHandler(PathHandler):
    """glob tag, include a list of file as a sequence node."""

    tag_pattern = '^(glob)$'

    def load(self, context: ILoadingContext, field: IBaseField) \
            -> Any:
        """See Resolver.resolve for usage."""
        if not context.expect_scalar(
            _('glob must be set on a scalar node')
        ):
            return LOADING_FAILED

        node = context.current_node()
        glob = node.value
        result = []
        for root in self._get_roots(context):
            for path in root.glob(glob):
                if not path.is_file():
                    continue

                content = self._load_file(context, path)

                if content is not None:
                    result.append(content)

        fake_node = SequenceNode('', result, node.start_mark, node.end_mark)
        return context.load(field, fake_node)
