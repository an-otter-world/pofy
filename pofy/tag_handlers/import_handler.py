"""Tag handler used to import files in YAML documents."""
from gettext import gettext as _
from pathlib import Path
from typing import List
from typing import Optional
from yaml import Node
from yaml import compose
from yaml.parser import ParserError

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
        for root_it in roots:
            assert isinstance(root_it, Path), \
                _('roots must be a list of Path objects')

        super().__init__()
        self._roots = roots

    def transform(self, context: LoadingContext) -> Optional[Node]:
        """See Resolver.resolve for usage."""
        if not context.expect_scalar(
            _('import / try-import must be set on a scalar node')
        ):
            return None

        node = context.current_node()
        file_path = Path(node.value)

        for root in self._roots:
            path = root / file_path
            if not path.is_file():
                continue

            with open(path, 'r') as yaml_file:
                try:
                    content = compose(yaml_file)
                    return content
                except ParserError as error:
                    context.error(
                        ErrorCode.VALUE_ERROR,
                        _('Parse error while loading {} : {}'),
                        path,
                        error
                    )
                    return None

        if node.tag == '!import':
            context.error(
                ErrorCode.IMPORT_NOT_FOUND,
                _('Unable to find {} in any of the configured directories'),
                path
            )

        return None
