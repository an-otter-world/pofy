"""Loading context tests."""
from pytest import raises
from yaml import Node

from pofy import ErrorCode
from pofy import PofyError
from pofy import TagHandler
from pofy.loading_context import LoadingContext

from tests.fixtures import mock_loading_context


def test_loading_context_raises():
    """Test loading context raises an error when no error_handler is set."""
    context = LoadingContext(error_handler=None, tag_handlers=[])

    with context.load(Node('', 'some_value', None, None)):
        with raises(PofyError):
            context.error(0, 'Test message')


def test_loading_context_calls_error_handler():
    """Test loading context raises an error when no error_handler is set."""
    with mock_loading_context(expected_error=0) as context:
        context.error(0, 'Message')
