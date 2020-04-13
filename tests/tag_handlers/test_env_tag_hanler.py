"""Env handler tests."""
from os import environ
from typing import Any
from typing import Optional

from pofy.common import ErrorCode
from pofy.common import UNDEFINED
from pofy.fields.string_field import StringField
from pofy.tag_handlers.env_handler import EnvHandler

from tests.helpers import check_load


def _check_tag(yaml: str, expected: Any) -> None:
    result = check_load(
        yaml,
        field=StringField(),
        tag_handlers=[EnvHandler()]
    )
    assert result == expected


def _check_tag_error(
    yaml: str,
    expected_error: Optional[ErrorCode] = None
) -> None:
    result = check_load(
        yaml,
        field=StringField(),
        expected_error=expected_error,
        tag_handlers=[EnvHandler()]
    )
    assert result == UNDEFINED


def test_env_tag_handler() -> None:
    """Env tag should correctly load environment variables."""
    environ['TEST_VARIABLE'] = 'test_value'
    _check_tag('!env TEST_VARIABLE', 'test_value')


def test_env_tag_handler_error_handling() -> None:
    """Env tag should handle errors correctly."""
    _check_tag_error('!env []', ErrorCode.UNEXPECTED_NODE_TYPE)
    _check_tag_error('!env {}', ErrorCode.UNEXPECTED_NODE_TYPE)

    # Shouldn't emit an error
    _check_tag('!env I_HOPE_YOU_DIDNT_SET_THIS_ONE', UNDEFINED)
