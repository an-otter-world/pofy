"""Loading context tests."""
from pytest import raises
from yaml import Node

from pofy import PofyError
from pofy.loading_context import LoadingContext


def test_loading_context_raises():
    """Test loading context raises an error when no error_handler is set."""
    context = LoadingContext(error_handler=None, tag_handlers=[])

    with context.load(Node('', 'some_value', None, None)):
        with raises(PofyError):
            context.error(0, 'Test message')


def test_loading_context_calls_error_handler():
    """Test loading context raises an error when no error_handler is set."""
    handler_called = False

    def _handler(node, code, message):
        nonlocal handler_called
        handler_called = True
        assert node.value == 'value'
        assert code == 0
        assert message == 'Message'

    context = LoadingContext(error_handler=_handler, tag_handlers=[])
    with context.load(Node('', 'value', None, None)):
        context.error(0, 'Message')
    assert handler_called
