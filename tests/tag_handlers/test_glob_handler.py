"""Glob handler tests."""
from pathlib import Path
from typing import Iterable

from pofy import ErrorCode
from pofy import GlobHandler
from pofy import ListField
from pofy import StringField

from tests.helpers import check_load


def _check_tag(
    yaml: str,
    expected_value: Iterable[str],
    allow_relative=True,
    location: Path = None,
    root: Path = None
):
    result = check_load(
        yaml,
        field=ListField(StringField()),
        tag_handlers=[
            GlobHandler(
                roots=[] if root is None else [root],
                allow_relative=allow_relative
            )
        ],
        location=str(location)
    )

    assert sorted(result) == sorted(expected_value)


def _check_tag_error(
    yaml: str,
    expected_error: ErrorCode,
    root: Path = None
):
    check_load(
        yaml,
        field=ListField(StringField()),
        expected_error=expected_error,
        tag_handlers=[
            GlobHandler(
                roots=[] if root is None else [root],
            )
        ],
    )


def test_glob_tag(datadir):
    """Glob tag should load globbed files if set correctly."""
    _check_tag(
        '!glob folder/**/*',
        ['file_1', 'file_2'],
        root=datadir
    )

    _check_tag(
        '!glob folder/**/*',
        ['file_1', 'file_2'],
        location=str(datadir / 'parent_file.yaml')
    )

    _check_tag(
        '!glob folder/**/*',
        [],
        location=str(datadir / 'parent_file.yaml'),
        allow_relative=False
    )


def test_glob_tag_error_handling(datadir):
    """Glob tag should correctly handle errors."""
    _check_tag_error('!glob []', ErrorCode.UNEXPECTED_NODE_TYPE)
    _check_tag_error('!glob {}', ErrorCode.UNEXPECTED_NODE_TYPE)
    _check_tag_error('!glob yaml_error.yaml', ErrorCode.VALUE_ERROR, datadir)
