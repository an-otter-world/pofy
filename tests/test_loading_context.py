"""Loading context tests."""
from pytest import raises

from pyyo import PyyoError
from pyyo.loading_context import LoadingContext


def test_loading_context_raises():
    """Test loading context raises an error when no error_handler is set."""
    context = LoadingContext(error_handler=None, resolvers=[])

    with raises(PyyoError):
        context.error(None, 0, 'Test message')


def test_loading_context_calls_error_handler():
    """Test loading context raises an error when no error_handler is set."""
    handler_called = False

    def _handler(node, code, message):
        nonlocal handler_called
        handler_called = True
        assert node == 'Node'
        assert code == 0
        assert message == 'Message'

    context = LoadingContext(error_handler=_handler, resolvers=[])
    context.error('Node', 0, 'Message')
    assert handler_called
