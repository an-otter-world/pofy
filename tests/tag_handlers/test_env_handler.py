"""Env handler tests."""
from os import environ
from typing import Any
from typing import Type

from yaml import MappingNode
from yaml import ScalarNode
from yaml import SequenceNode

from pofy import EnvHandler
from pofy import ErrorCode
from pofy.common import LOADING_FAILED

from tests.helpers import load_node


def _check_tag(node_value: str, expected: Any):
    result = load_node(
        node=ScalarNode('!env', node_value, None, None),
        tag_handlers=[EnvHandler()]
    )
    assert result == expected


def _check_tag_error(
    node_value: str,
    node_type: Type = ScalarNode,
    expected_error: ErrorCode = None
):
    result = load_node(
        node=node_type('!env', node_value, None, None),
        expected_error=expected_error,
        tag_handlers=[EnvHandler()]
    )
    assert result == LOADING_FAILED


def test_env_tag():
    """Env tag should correctly load environment variables."""
    environ['TEST_VARIABLE'] = 'test_value'
    _check_tag('TEST_VARIABLE', 'test_value')


def test_env_tag_error_handling():
    """Env tag should handle errors correctly."""
    _check_tag_error([], SequenceNode, ErrorCode.UNEXPECTED_NODE_TYPE)
    _check_tag_error([], MappingNode, ErrorCode.UNEXPECTED_NODE_TYPE)

    # Shouldn't emit an error
    _check_tag('I_HOPE_YOU_DIDNT_SET_THIS_ONE', LOADING_FAILED)
