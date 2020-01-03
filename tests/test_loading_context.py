"""Loading context tests."""
from pytest import raises
from yaml import Node
from yaml.error import Mark

from pofy import ErrorCode
from pofy import PofyValueError
from pofy import TagHandler
from pofy.loading_context import LoadingContext

from tests.fixtures import mock_loading_context


def test_loading_context_raises():
    """Test loading context raises an error when no error_handler is set."""
    context = LoadingContext(error_handler=None, tag_handlers=[])

    node = Node(
        'tag',
        'value',
        Mark('file_name', 0, 10, 42, None, None),
        Mark('file_name', 0, 12, 32, None, None)
    )

    with context.load(node):
        with raises(PofyValueError):
            context.error(ErrorCode.VALUE_ERROR, 'Test message')


def test_loading_context_calls_error_handler():
    """Test loading context raises an error when no error_handler is set."""
    with mock_loading_context(expected_error=0) as context:
        context.error(0, 'Message')


def test_loading_context_raises_on_multiple_tag_match():
    """Test loading context raises an error a tag is ambigous."""
    class _DummyHandler(TagHandler):
        tag_pattern = '^dummy$'

        def transform(self, context):
            return context.current_node()

    with mock_loading_context(
        node=Node('!dummy', '', None, None),
        expected_error=ErrorCode.MULTIPLE_MATCHING_HANDLERS,
        tag_handlers=[
            _DummyHandler(),
            _DummyHandler()
        ]
    ):
        pass
