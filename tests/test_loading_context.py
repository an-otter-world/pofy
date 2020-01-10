"""Loading context tests."""
from pytest import raises
from yaml import Node
from yaml.error import Mark

from pofy import BaseField
from pofy import ErrorCode
from pofy import PofyValueError
from pofy import TagHandler
from pofy.loading_context import LoadingContext

from tests.helpers import load_node


def test_loading_context_raises():
    """Loading context should raise on error when no error_handler is set."""
    context = LoadingContext(error_handler=None, tag_handlers=[])

    class _RaisingField(BaseField):
        def _load(self, context):
            context.error(ErrorCode.VALUE_ERROR, 'Test message')

    with raises(PofyValueError):
        context.load(_RaisingField(), _get_dummy_node())


def test_loading_context_raises_on_multiple_tag_match():
    """Loading context should emit an error a tag is ambigous."""
    class _DummyHandler(TagHandler):
        tag_pattern = '^dummy$'

        def load(self, context, field):
            return context.current_node()

    load_node(
        node=Node('!dummy', '', None, None),
        expected_error=ErrorCode.MULTIPLE_MATCHING_HANDLERS,
        tag_handlers=[
            _DummyHandler(),
            _DummyHandler()
        ]
    )


def test_loading_context_returns_node_location():
    """Loading context should store the last given location for a node."""
    def _check(location):
        class _ChildField(BaseField):
            def _load(self, context):
                assert context.current_location() == location

        class _ParentField(BaseField):
            def _load(self, context):
                context.load(_ChildField(), _get_dummy_node())

        context = LoadingContext(error_handler=None, tag_handlers=[])
        context.load(_ParentField(), _get_dummy_node(), location)

    _check('/some/location')

    # This should go all the way up in the node stack and finally return None
    _check(None)


def _get_dummy_node():
    return Node(
        'tag',
        'value',
        Mark('file_name', 0, 10, 42, None, None),
        Mark('file_name', 0, 12, 32, None, None)
    )
