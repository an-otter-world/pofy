"""Tag handler used to import files in YAML documents."""
from gettext import gettext as _
from pathlib import Path
from typing import List
from yaml import Node
from yaml import SequenceNode
from yaml import compose
from yaml.parser import ParserError

from pofy.errors import ErrorCode
from pofy.loading_context import LoadingContext

from .tag_handler import TagHandler


class GlobHandler(TagHandler):
    """Include a YAML document.

    Will replace the tagged node by the loaded document.
    """

    tag_pattern = '^(glob)$'

    def __init__(self, roots: List[Path]):
        """Initialize GlobHandler.

        Args:
            roots: Roots paths to use when resolving files.

        """
        super().__init__()
        self._roots = roots

    def transform(self, context: LoadingContext) -> Node:
        """See Resolver.resolve for usage."""
        if not context.expect_scalar(
            _('glob must be set on a scalar node')
        ):
            return None

        node = context.current_node()
        glob = node.value
        result = []
        for root in self._roots:
            for path in root.glob(glob):
                if not path.is_file():
                    continue

                with open(path, 'r') as yaml_file:
                    try:
                        content = compose(yaml_file)
                        result.append(content)
                    except ParserError as error:
                        context.error(
                            ErrorCode.VALUE_ERROR,
                            _('Parse error while loading {} : {}'),
                            path,
                            error
                        )
                        return None

        return SequenceNode('', result, node.start_mark, node.end_mark)
