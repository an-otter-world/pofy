"""Helpers to test path handlers."""
from pathlib import Path
from typing import Any
from typing import List
from typing import Type

from pofy import ErrorCode
from pofy import LOADING_FAILED
from pofy import StringField
from pofy import ListField
from pofy import PathHandler

from tests.helpers import check_load


def check_path_tag(
    handler_type: Type[PathHandler],
    yaml: str,
    expected_value: Any,
    allow_relative=True,
    location: Path = None,
    roots: List[Path] = None
):
    """Path tag hanhler inherited tags test helper."""
    result = check_load(
        yaml,
        field=ListField(StringField()),
        tag_handlers=[
            handler_type(
                roots=[] if roots is None else roots,
                allow_relative=allow_relative
            )
        ],
        location=str(location)
    )

    # for glob tag handler.
    if isinstance(expected_value, list):
        assert sorted(result) == sorted(expected_value)
    else:
        assert result == expected_value


def check_path_tag_error(
    handler_type: Type[PathHandler],
    yaml: str,
    expected_error: ErrorCode,
    location: str = None,
    allow_relative=True,
    roots: List[Path] = None,
    expected_value=LOADING_FAILED
):
    """Path tag hanhler inherited tags error test helper."""
    result = check_load(
        yaml,
        field=ListField(StringField()),
        expected_error=expected_error,
        location=location,
        tag_handlers=[
            handler_type(
                roots=[] if roots is None else roots,
                allow_relative=allow_relative
            )
        ],
    )

    assert result == expected_value
