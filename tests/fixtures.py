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
    object_class: Type,
    source: Union[AnyStr, IO[str]],
    tag_handlers: List[TagHandler] = None
):
    """Load the given object, expecting an error to be raised."""
    error_raised = False

    def _on_error(__, error, ___):
        nonlocal error_raised
        error_raised = True
        assert error == expected_error

    load(
        object_class,
        source,
        error_handler=_on_error,
        tag_handlers=tag_handlers
    )


def load_with_fail_tag(
    object_class: Type,
    source: Union[AnyStr, IO[str]]
):
    """Load the given object, expecting an error to be raised."""
    class _FailTagHandler(TagHandler):
        tag_pattern = '^fail$'

        def transform(self, _):
            """TagHandler.transform implementation."""
            return None

    return load(
        object_class,
        source,
        tag_handlers=[_FailTagHandler()]
    )
