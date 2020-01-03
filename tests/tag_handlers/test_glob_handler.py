"""Glob handler tests."""
from yaml import SequenceNode
from yaml import ScalarNode

from pofy import ErrorCode
from pofy import GlobHandler

from tests.fixtures import load_node


def test_bad_node_for_glob_raises():
    """Test glob tag on a not-scalar node raise an error."""
    load_node(
        node=SequenceNode('!glob', '', None, None),
        expected_error=ErrorCode.UNEXPECTED_NODE_TYPE,
        tag_handlers=[GlobHandler([])]
    )


def test_glob_resolves_correctly(datadir):
    """Test glob resolves correctly files."""
    handler = GlobHandler([datadir])
    loaded_nodes = load_node(
        node=ScalarNode('!glob', 'folder/**/*', None, None),
        tag_handlers=[handler]
    )

    assert len(loaded_nodes) == 2
    assert loaded_nodes[0].value in ['file2_content', 'file3_content']
    assert loaded_nodes[1].value in ['file2_content', 'file3_content']


def test_glob_raise_error_on_yaml_load_failure(datadir):
    """Test glob raises a VALUE_ERROR if a file can't be deserialized."""
    handler = GlobHandler([datadir])
    load_node(
        node=ScalarNode('!glob', '**/*', None, None),
        expected_error=ErrorCode.VALUE_ERROR,
        tag_handlers=[handler]
    )
