"""Tag handler used to import files in YAML documents."""
from abc import abstractmethod
from gettext import gettext as _
from pathlib import Path
from typing import Any
from typing import Iterator
from typing import List
from typing import Optional
from typing import cast

from yaml import Node
from yaml import compose
from yaml.parser import ParserError

from pofy.common import ErrorCode
from pofy.interfaces import IBaseField
from pofy.interfaces import ILoadingContext
from pofy.tag_handlers.tag_handler import TagHandler


class PathHandler(TagHandler):
    """Base class for handlers that handle pathes relative to root directories.

    Allow getting root directories, either from a given list, or relatively to
    the current loaded YAML document, if possible.
    """

    def __init__(
        self,
        roots: Optional[List[Path]] = None,
        allow_relative: bool = True
    ):
        """Initialize the PathHandler.

        Args:
            roots: Roots paths to use when resolving files.
            allow_relative: If set to True, the handler will try to load files
                            relative to the current YAML file, if applicable.

        """
        if roots is not None:
            for root_it in roots:
                assert isinstance(root_it, Path), \
                    _('roots must be a list of Path objects')

        super().__init__()
        self._roots = roots
        self._allow_relative = allow_relative

    @abstractmethod
    def load(self, context: ILoadingContext, field: IBaseField) -> Any:
        raise NotImplementedError

    def _get_roots(self, context: ILoadingContext) -> Iterator[Path]:
        """Return the configured root directories."""
        if self._allow_relative:
            current_location = context.current_location()
            if current_location is not None:
                file_path = Path(current_location)
                parent = file_path.parent
                if parent.is_dir():
                    yield parent

        if self._roots is not None:
            for root in self._roots:
                yield root

    @staticmethod
    def _load_file(context: ILoadingContext, path: Path) -> Optional[Node]:
        """Load a YAML document, emit a PofyError on ParseError."""
        with open(path, 'r') as yaml_file:
            try:
                return cast(Node, compose(yaml_file)) # type: ignore
            except ParserError as error:
                context.error(
                    ErrorCode.VALUE_ERROR,
                    _('Parse error while loading {} : {}'),
                    path,
                    error
                )
        return None
