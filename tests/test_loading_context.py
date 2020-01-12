"""Loading context tests."""
from typing import Optional

from pytest import raises
from yaml import Node
from yaml.error import Mark

from pofy.common import ErrorCode
from pofy.common import PofyValueError
from pofy.fields.base_field import BaseField
from pofy.interfaces import IBaseField
from pofy.interfaces import ILoadingContext
from pofy.loading_context import LoadingContext
from pofy.tag_handlers.tag_handler import TagHandler

from tests.helpers import check_load


def test_loading_context_raises() -> None:
    """Loading context should raise on error when no error_handler is set."""
    context = LoadingContext(error_handler=None, tag_handlers=[])

    class _RaisingField(BaseField):
        def _load(self, context: ILoadingContext) -> None:
            context.error(ErrorCode.VALUE_ERROR, 'Test message')

    with raises(PofyValueError):
        context.load(_RaisingField(), _get_dummy_node())


def test_loading_context_raises_on_multiple_tag_match() -> None:
    """Loading context should emit an error a tag is ambigous."""
    class _DummyHandler(TagHandler):
        tag_pattern = '^dummy$'

        def load(self, context: ILoadingContext, field: IBaseField) -> Node:
            return context.current_node()

    check_load(
        '!dummy value',
        str,
        expected_error=ErrorCode.MULTIPLE_MATCHING_HANDLERS,
        tag_handlers=[
            _DummyHandler(),
            _DummyHandler()
        ]
    )


def test_loading_context_returns_node_location() -> None:
    """Loading context should store the last given location for a node."""
    def _check(location: Optional[str]) -> None:
        class _ChildField(BaseField):
            def _load(self, context: ILoadingContext) -> None:
                assert context.current_location() == location

        class _ParentField(BaseField):
            def _load(self, context: ILoadingContext) -> None:
                context.load(_ChildField(), _get_dummy_node())

        context = LoadingContext(error_handler=None, tag_handlers=[])
        context.load(_ParentField(), _get_dummy_node(), location)

    _check('/some/location')

    # This should go all the way up in the node stack and finally return None
    _check(None)


def _get_dummy_node() -> Node:
    return Node(
        'tag',
        'value',
        Mark('file_name', 0, 10, 42, None, None),
        Mark('file_name', 0, 12, 32, None, None)
    )
