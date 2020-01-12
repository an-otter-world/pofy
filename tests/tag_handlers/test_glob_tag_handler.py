"""Glob handler tests."""
from pathlib import Path

from pofy.common import ErrorCode
from pofy.tag_handlers.glob_handler import GlobHandler

from tests.tag_handlers.path_handler_helpers import check_path_tag
from tests.tag_handlers.path_handler_helpers import check_path_tag_error


def test_glob_tag_handler(datadir: Path) -> None:
    """Glob tag should load globbed files if set correctly."""
    check_path_tag(
        GlobHandler,
        '!glob folder/**/*',
        ['file_1', 'file_2'],
        roots=[datadir]
    )

    check_path_tag(
        GlobHandler,
        '!glob folder/**/*',
        ['file_1', 'file_2'],
        location=datadir / 'parent_file.yaml'
    )

    check_path_tag(
        GlobHandler,
        '!glob folder/**/*',
        [],
        location=datadir / 'parent_file.yaml',
        allow_relative=False
    )


def test_glob_tag_handler_error_handling(datadir: Path) -> None:
    """Glob tag should correctly handle errors."""
    check_path_tag_error(
        GlobHandler,
        '!glob []',
        ErrorCode.UNEXPECTED_NODE_TYPE
    )

    check_path_tag_error(
        GlobHandler,
        '!glob {}',
        ErrorCode.UNEXPECTED_NODE_TYPE
    )

    check_path_tag_error(
        GlobHandler,
        '!glob yaml_error.yaml',
        ErrorCode.VALUE_ERROR,
        roots=[datadir],
        expected_value=[]
    )
