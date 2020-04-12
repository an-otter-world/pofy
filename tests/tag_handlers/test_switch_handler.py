"""If handler tests."""
from typing import Any
from typing import Optional

from pofy.common import LOADING_FAILED
from pofy.fields.string_field import StringField
from pofy.tag_handlers.switch_handler import SwitchHandler
from pofy.common import ErrorCode

from tests.helpers import check_load


def _check_switch_tag(
    yaml: str,
    expected_value: Any = None,
    expected_error: Optional[ErrorCode] = None
) -> None:
    if expected_error is not None:
        expected_value = LOADING_FAILED

    result = check_load(
        yaml,
        field=StringField(),
        tag_handlers=[
            SwitchHandler()
        ],
        expected_error=expected_error
    )

    assert result == expected_value


def test_if_tag_handler() -> None:
    """Env tag should correctly load ifironment variables."""
    _check_switch_tag(
        '!switch [!fail value_1, !fail value_2, value_3]',
        'value_3'
    )

    _check_switch_tag(
        '!switch [!fail value_1, !fail value_2, !fail value_3]',
        LOADING_FAILED
    )


def test_switch_tag_handler_error_handling() -> None:
    """Switch tag should correctly handle errors."""
    _check_switch_tag(
        '!switch scalar_value',
        expected_error=ErrorCode.UNEXPECTED_NODE_TYPE
    )

    _check_switch_tag(
        '!switch {}',
        expected_error=ErrorCode.UNEXPECTED_NODE_TYPE
    )
