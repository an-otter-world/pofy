"""Tag handler used to import files in YAML documents."""
from gettext import gettext as _
from pathlib import Path
from typing import Any
from typing import Optional

from pofy.common import ErrorCode
from pofy.common import UNDEFINED
from pofy.interfaces import IBaseField
from pofy.interfaces import ILoadingContext
from pofy.tag_handlers.path_handler import PathHandler


class ImportHandler(PathHandler):
    """Include a YAML document.

    Will replace the tagged node by the loaded document.
    """

    tag_pattern = '^(try-import|import)$'

    def load(self, context: ILoadingContext, field: IBaseField) -> Any:
        """See Resolver.resolve for usage."""
        if not context.expect_scalar(
            _('import / try-import must be set on a scalar node')
        ):
            return UNDEFINED

        file_path = self._get_file(context)
        if file_path is None:
            node = context.current_node()
            if node.tag == '!import':
                context.error(
                    ErrorCode.IMPORT_NOT_FOUND,
                    _('Unable to find {} in any of the configured directories'),
                    node.value
                )

            return UNDEFINED

        file_yaml_node = self._load_file(context, file_path)

        if file_yaml_node is None:
            return UNDEFINED

        return context.load(field, file_yaml_node, str(file_path))

    def _get_file(self, context: ILoadingContext) -> Optional[Path]:
        node = context.current_node()
        file_path = Path(node.value)

        if file_path.is_absolute():
            return file_path

        for root in self._get_roots(context):
            path = root / file_path
            if path.is_file():
                return path

        return None
