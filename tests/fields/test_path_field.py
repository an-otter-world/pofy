"""Path field tests."""
from pathlib import Path

from pofy import ErrorCode
from pofy import PathField
from pofy import load

from tests.fixtures import expect_load_error


class _PathObject:

    class Schema:
        """Pofy fields."""

        path_field = PathField()
        not_checked_path_field = PathField(must_exist=False)


def test_path_field_load_absolute_path(datadir: Path):
    """Test path field loading works."""
    path = datadir / 'some_file.txt'
    test = load('path_field: {}'.format(path), _PathObject)
    assert test.path_field == path


def test_path_field_load_relative_path(datadir: Path):
    """Test path field loading works."""
    with open(datadir / 'file.yaml', 'r') as yaml_file:
        test = load(yaml_file, _PathObject)
        assert test.path_field == datadir / 'some_file.txt'


def test_path_field_on_bad_node_error():
    """Test not-scalar node for a path field raise an error."""
    expect_load_error(
        ErrorCode.UNEXPECTED_NODE_TYPE,
        'path_field: ["a", "list"]',
        _PathObject
    )


def test_path_field_must_exist():
    """Test the must exist flag on PathField behaves correctly."""
    test = expect_load_error(
        ErrorCode.VALIDATION_ERROR,
        'path_field: doesnt_exist.txt',
        _PathObject
    )
    assert not hasattr(test, 'path_field')

    test = load('not_checked_path_field: doesnt_exist.txt', _PathObject)
    assert test.not_checked_path_field == Path('doesnt_exist.txt')
