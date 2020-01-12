"""Path field tests."""
from pathlib import Path

from pofy.common import ErrorCode
from pofy.fields.path_field import PathField

from tests.helpers import check_field
from tests.helpers import check_field_error
from tests.helpers import check_load


class _PathObject:

    class Schema:
        """Pofy fields."""

        field = PathField()
        not_checked = PathField(must_exist=False)


def _check_field(yaml_value: str, expected_value: Path) -> None:
    check_field(_PathObject, 'field', yaml_value, expected_value)


def _check_field_error(yaml_value: str, expected_error: ErrorCode) -> None:
    check_field_error(_PathObject, 'field', yaml_value, expected_error)


def test_path_field(datadir: Path) -> None:
    """Path field should load correct values."""
    # Absolute path
    file_path = datadir / 'some_file.txt'
    _check_field(str(file_path), file_path)

    # Relative path
    file_path = datadir / 'file.yaml'
    with open(file_path, 'r') as yaml_file:
        result = check_load(yaml_file, _PathObject, location=str(file_path))
        assert result.field == datadir / 'some_file.txt'

    result = check_load('not_checked: doesnt_exists.txt', _PathObject)
    assert result.not_checked == Path('doesnt_exists.txt')


def test_path_field_error_handling() -> None:
    """Path field should correctly handle errors."""
    _check_field_error('[a, list]', ErrorCode.UNEXPECTED_NODE_TYPE)
    _check_field_error('{a: dict}', ErrorCode.UNEXPECTED_NODE_TYPE)
    _check_field_error('doesnt_exists.txt', ErrorCode.VALIDATION_ERROR)
