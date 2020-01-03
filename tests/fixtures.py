"""Test fixtures & dummy classes."""
from contextlib import contextmanager
from typing import IO
from typing import List
from typing import Optional
from typing import Type
from typing import Union

from yaml import Node

from pofy import ErrorCode
from pofy import LoadingContext
from pofy import TagHandler
from pofy import load


def expect_load_error(
    expected_error: ErrorCode,
    source: Union[str, IO[str]],
    object_class: Type,
    tag_handlers: List[TagHandler] = None
):
    """Load the given object, expecting an error to be raised."""
    error_raised = False

    def _on_error(__: Node, error: ErrorCode, ___: str):
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
    source: Union[str, IO[str]],
    object_class: Type,
) -> Optional[object]:
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


@contextmanager
def mock_loading_context(
    expected_error: Optional[int] = None,
    tag_handlers: Optional[List[TagHandler]] = None,
    node: Node = None
):
    """Load the given object, expecting an error to be raised."""
    handler_called = False

    def _handler(__: Node, code: ErrorCode, ___: str):
        nonlocal handler_called
        handler_called = True
        assert expected_error is not None
        assert code == expected_error

    if tag_handlers is None:
        tag_handlers = []

    context = LoadingContext(
        error_handler=_handler,
        tag_handlers=tag_handlers
    )

    if node is None:
        node = Node('', '', None, None)

    with context.load(node):
        yield context

    if expected_error is not None:
        assert handler_called
