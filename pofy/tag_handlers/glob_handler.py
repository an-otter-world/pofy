"""Tag handler used to import files in YAML documents."""
from gettext import gettext as _
from pathlib import Path
from typing import List
from typing import Any
from yaml import SequenceNode
from yaml import compose
from yaml.parser import ParserError

from pofy.common import LOADING_FAILED
from pofy.errors import ErrorCode
from pofy.common import ILoadingContext
from pofy.common import IBaseField

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
        for root_it in roots:
            assert isinstance(root_it, Path), \
                _('roots must be a list of Path objects')

        self._roots = roots

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

        fake_node = SequenceNode('', result, node.start_mark, node.end_mark)
        return context.load(field, fake_node)
