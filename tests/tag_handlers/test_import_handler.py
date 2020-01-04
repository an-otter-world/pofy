"""Glob handler tests."""
from pathlib import Path
from yaml import ScalarNode
from yaml import SequenceNode

from pofy.common import LOADING_FAILED
from pofy import ErrorCode
from pofy import ImportHandler

from tests.helpers import load_node


def test_import_tag_works(datadir):
    """Test import tag on a non-scalar node raise an error."""
    def _check_tag(tag):
        result = load_node(
            node=ScalarNode(tag, 'file1.yaml', None, None),
            tag_handlers=[ImportHandler([datadir])]
        )
        assert result == 'file1_content'

    _check_tag('!import')
    _check_tag('!try-import')


def test_bad_import_node_raises():
    """Test import tag on a non-scalar node raise an error."""
    load_node(
        node=SequenceNode('!import', '', None, None),
        expected_error=ErrorCode.UNEXPECTED_NODE_TYPE,
        tag_handlers=[ImportHandler([])]
    )


def test_import_tag_ignore_directories(datadir):
    """Test import tag ignores directories."""
    handlers = [
        ImportHandler([
            datadir / 'test_ignore_dir' / 'root_1',
            datadir / 'test_ignore_dir' / 'root_2'
        ])
    ]
    result = load_node(
        node=ScalarNode('!import', 'file.yaml', None, None),
        tag_handlers=handlers
    )
    assert result == 'file_content'


def test_import_on_unexisting_file(datadir):
    """Test import behaves correctly when imported file doesn't exists."""
    handlers = [
        ImportHandler([datadir])
    ]

    load_node(
        node=ScalarNode('!import', 'doesnt_exists.yaml', None, None),
        expected_error=ErrorCode.IMPORT_NOT_FOUND,
        tag_handlers=handlers
    )

    result = load_node(
        node=ScalarNode('!try-import', 'doesnt_exists.yaml', None, None),
        tag_handlers=handlers
    )

    assert result == LOADING_FAILED


def test_import_on_parse_error(datadir):
    """Test parse error with import tag raise a value error."""
    handlers = [
        ImportHandler([datadir])
    ]

    load_node(
        node=ScalarNode('!import', 'corrupted.yaml', None, None),
        expected_error=ErrorCode.VALUE_ERROR,
        tag_handlers=handlers
    )


def test_relative_import(datadir: Path):
    """Test import works with paths relative to the loaded file."""
    value = load_node(
        node=ScalarNode('!import', 'file1.yaml', None, None),
        tag_handlers=[ImportHandler(allow_relative=True)],
        location=str(datadir / 'parent_file.yaml')
    )

    assert value == 'file1_content'

    load_node(
        node=ScalarNode('!import', 'file1.yaml', None, None),
        tag_handlers=[ImportHandler(allow_relative=False)],
        expected_error=ErrorCode.IMPORT_NOT_FOUND,
        location=str(datadir / 'parent_file.yaml')
    )


def test_absolute_import(datadir: Path):
    """Test import works with absolute paths."""
    assert datadir.is_absolute()
    value = load_node(
        node=ScalarNode('!import', str(datadir / 'file1.yaml'), None, None),
        tag_handlers=[ImportHandler()]
    )

    assert value == 'file1_content'
