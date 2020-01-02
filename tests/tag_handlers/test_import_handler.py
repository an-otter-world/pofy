"""Glob handler tests."""
from yaml import SequenceNode
from yaml import ScalarNode

from pofy import ErrorCode
from pofy import ImportHandler

from tests.fixtures import mock_loading_context


def test_import_tag_works(datadir):
    """Test import tag on a non-scalar node raise an error."""
    def _check_tag(tag):
        with mock_loading_context(
            node=ScalarNode(tag, 'file1.yaml', None, None),
            tag_handlers=[ImportHandler([datadir])]
        ) as context:
            node = context.current_node()
            assert isinstance(node, ScalarNode)
            assert node.value == 'file1_content'

    _check_tag('!import')
    _check_tag('!try-import')


def test_bad_import_node_raises():
    """Test import tag on a non-scalar node raise an error."""
    with mock_loading_context(
        node=SequenceNode('!import', '', None, None),
        expected_error=ErrorCode.UNEXPECTED_NODE_TYPE,
        tag_handlers=[ImportHandler([])]
    ):
        pass


def test_import_tag_ignore_directories(datadir):
    """Test import tag ignores directories."""
    handlers = [
        ImportHandler([
            datadir / 'test_ignore_dir' / 'root_1',
            datadir / 'test_ignore_dir' / 'root_2'
        ])
    ]
    with mock_loading_context(
        node=ScalarNode('!import', 'file.yaml', None, None),
        tag_handlers=handlers
    ) as context:
        node = context.current_node()
        assert isinstance(node, ScalarNode)
        assert node.value == 'file_content'


def test_import_on_unexisting_file(datadir):
    """Test import behaves correctly when imported file doesn't exists."""
    handlers = [
        ImportHandler([datadir])
    ]

    with mock_loading_context(
        node=ScalarNode('!import', 'doesnt_exists.yaml', None, None),
        expected_error=ErrorCode.IMPORT_NOT_FOUND,
        tag_handlers=handlers
    ):
        pass

    with mock_loading_context(
        node=ScalarNode('!try_import', 'doesnt_exists.yaml', None, None),
        tag_handlers=handlers
    ):
        pass


def test_import_on_parse_error(datadir):
    """Test parse error with import tag raise a value error."""
    handlers = [
        ImportHandler([datadir])
    ]

    with mock_loading_context(
        node=ScalarNode('!import', 'corrupted.yaml', None, None),
        expected_error=ErrorCode.VALUE_ERROR,
        tag_handlers=handlers
    ):
        pass
