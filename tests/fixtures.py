"""Test fixtures & dummy classes."""
from typing import AnyStr
from typing import IO
from typing import List
from typing import Type
from typing import Union

from pofy import ErrorCode
from pofy import TagHandler
from pofy import load


def expect_load_error(
    expected_error: ErrorCode,
    source: Union[AnyStr, IO[str]],
    object_class: Type,
    tag_handlers: List[TagHandler] = None
):
    """Load the given object, expecting an error to be raised."""
    error_raised = False

    def _on_error(__, error, ___):
        nonlocal error_raised
        error_raised = True
        assert error == expected_error

    load(
        source,
        object_class,
        error_handler=_on_error,
        tag_handlers=tag_handlers
    )


def load_with_fail_tag(
    source: Union[AnyStr, IO[str]],
    object_class: Type,
):
    """Load the given object, expecting an error to be raised."""
    class _FailTagHandler(TagHandler):
        tag_pattern = '^fail$'

        def transform(self, _):
            """TagHandler.transform implementation."""
            return None

    return load(
        source,
        object_class,
        tag_handlers=[_FailTagHandler()]
    )
