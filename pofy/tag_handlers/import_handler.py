"""Tag handler used to import files in YAML documents."""
from gettext import gettext as _
from pathlib import Path
from typing import List
from yaml import Node
from yaml import ScalarNode
from yaml import compose

from pofy.errors import ErrorCode
from pofy.loading_context import LoadingContext

from .tag_handler import TagHandler


class ImportHandler(TagHandler):
    """Include a YAML document.

    Will replace the tagged node by the loaded document.
    """

    tag_pattern = '^(try-import|import)$'

    def __init__(self, roots: List[Path]):
        """Initialize Import Handler Base.

        Args:
            roots: Roots paths to use when resolving files.

        """
        super().__init__()
        self._roots = roots

    def transform(self, context: LoadingContext) -> Node:
        """See Resolver.resolve for usage."""
        node = context.current_node()
        if not isinstance(node, ScalarNode):
            context.error(
                ErrorCode.UNEXPECTED_NODE_TYPE,
                _('import / try-import must be set on a scalar node')
            )
            return None

        file_path = Path(node.value)

        for root in self._roots:
            path = root / file_path
            if not path.is_file():
                continue

            with open(path, 'r') as yaml_file:
                try:
                    content = compose(yaml_file)
                    return content
                finally:
                    pass

        if node.tag == '!import':
            context.error(
                ErrorCode.IMPORT_NOT_FOUND,
                _('Unable to find file {} in any of the configured directories')
            )

        return None
