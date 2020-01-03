"""Test fixtures & dummy classes."""
from typing import IO
from typing import List
from typing import Optional
from typing import Type
from typing import Union

from yaml import Node

from pofy import BaseField
from pofy import ErrorCode
from pofy import LoadingContext
from pofy import TagHandler
from pofy import load
from pofy.common import LOADING_FAILED


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

        def load(self, __, ___):
            """TagHandler.transform implementation."""
            return LOADING_FAILED

    return load(
        source,
        object_class,
        tag_handlers=[_FailTagHandler()]
    )


def load_node(
    expected_error: Optional[int] = None,
    tag_handlers: Optional[List[TagHandler]] = None,
    node: Node = None,
    location: Optional[str] = None
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

    if node is None:
        node = Node('', '', None, None)

    class _MockField(BaseField):
        def _load(self, context):
            return context.current_node().value

    context = LoadingContext(
        error_handler=_handler,
        tag_handlers=tag_handlers
    )

    result = context.load(_MockField(), node, location)

    if expected_error is not None:
        assert handler_called

    return result
