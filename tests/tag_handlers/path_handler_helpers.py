"""Helpers to test path handlers."""
from pathlib import Path
from typing import Any
from typing import List
from typing import Optional
from typing import Type

from pofy.common import ErrorCode
from pofy.common import LOADING_FAILED
from pofy.fields.list_field import ListField
from pofy.fields.string_field import StringField
from pofy.tag_handlers.path_handler import PathHandler

from tests.helpers import check_load


def check_path_tag(
    handler_type: Type[PathHandler],
    yaml: str,
    expected_value: Any,
    allow_relative: bool = True,
    location: Optional[Path] = None,
    roots: Optional[List[Path]] = None
) -> None:
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
    location: Optional[str] = None,
    allow_relative: bool = True,
    roots: Optional[List[Path]] = None,
    expected_value: Any = LOADING_FAILED
) -> None:
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
