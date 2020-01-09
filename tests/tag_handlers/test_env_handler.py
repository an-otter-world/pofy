"""Env handler tests."""
from os import environ
from typing import Any

from pofy import EnvHandler
from pofy import ErrorCode
from pofy import StringField
from pofy.common import LOADING_FAILED

from tests.helpers import check_load


def _check_tag(yaml: str, expected: Any):
    result = check_load(
        yaml,
        field=StringField(),
        tag_handlers=[EnvHandler()]
    )
    assert result == expected


def _check_tag_error(
    yaml: str,
    expected_error: ErrorCode = None
):
    result = check_load(
        yaml,
        field=StringField(),
        expected_error=expected_error,
        tag_handlers=[EnvHandler()]
    )
    assert result == LOADING_FAILED


def test_env_tag():
    """Env tag should correctly load environment variables."""
    environ['TEST_VARIABLE'] = 'test_value'
    _check_tag('!env TEST_VARIABLE', 'test_value')


def test_env_tag_error_handling():
    """Env tag should handle errors correctly."""
    _check_tag_error('!env []', ErrorCode.UNEXPECTED_NODE_TYPE)
    _check_tag_error('!env {}', ErrorCode.UNEXPECTED_NODE_TYPE)

    # Shouldn't emit an error
    _check_tag('!env I_HOPE_YOU_DIDNT_SET_THIS_ONE', LOADING_FAILED)
