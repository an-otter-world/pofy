"""Glob handler tests."""
from os import environ
from yaml import ScalarNode
from yaml import SequenceNode

from pofy import EnvHandler
from pofy import ErrorCode
from pofy.common import LOADING_FAILED

from tests.fixtures import load_node


def test_bad_node_for_env_raises():
    """Test glob tag on a not-scalar node raise an error."""
    load_node(
        node=SequenceNode('!env', '', None, None),
        expected_error=ErrorCode.UNEXPECTED_NODE_TYPE,
        tag_handlers=[EnvHandler()]
    )


def test_env_tag_handler():
    """Test glob resolves correctly files."""
    environ['TEST_VARIABLE'] = 'test_value'
    result = load_node(
        node=ScalarNode('!env', 'TEST_VARIABLE', None, None),
        tag_handlers=[EnvHandler()]
    )

    assert result == 'test_value'

    result = load_node(
        node=ScalarNode('!env', 'I_HOPE_YOU_DIDNT_SET_THIS_ONE', None, None),
        tag_handlers=[EnvHandler()]
    )
    assert result == LOADING_FAILED
