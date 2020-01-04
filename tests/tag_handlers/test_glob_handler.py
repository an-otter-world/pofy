"""Glob handler tests."""
from yaml import SequenceNode
from yaml import ScalarNode

from pofy import ErrorCode
from pofy import GlobHandler

from tests.helpers import load_node


def test_bad_node_for_glob_raises():
    """Test glob tag on a not-scalar node raise an error."""
    load_node(
        node=SequenceNode('!glob', '', None, None),
        expected_error=ErrorCode.UNEXPECTED_NODE_TYPE,
        tag_handlers=[GlobHandler()]
    )


def test_glob_resolves_correctly(datadir):
    """Test glob resolves correctly files."""
    loaded_nodes = load_node(
        node=ScalarNode('!glob', 'folder/**/*', None, None),
        tag_handlers=[GlobHandler([datadir])]
    )

    assert len(loaded_nodes) == 2
    assert loaded_nodes[0].value in ['file2_content', 'file3_content']
    assert loaded_nodes[1].value in ['file2_content', 'file3_content']


def test_glob_raise_error_on_yaml_load_failure(datadir):
    """Test glob raises a VALUE_ERROR if a file can't be deserialized."""
    load_node(
        node=ScalarNode('!glob', '**/*', None, None),
        expected_error=ErrorCode.VALUE_ERROR,
        tag_handlers=[GlobHandler([datadir])]
    )


def test_relative_glob(datadir):
    """Test glob works with relative paths."""
    value = load_node(
        node=ScalarNode('!glob', 'folder/**/*', None, None),
        tag_handlers=[GlobHandler(allow_relative=True)],
        location=str(datadir / 'parent_file.yaml')
    )

    assert len(value) == 2
    assert value[0].value in ['file2_content', 'file3_content']
    assert value[1].value in ['file2_content', 'file3_content']

    value = load_node(
        node=ScalarNode('!glob', 'folder/**/*', None, None),
        tag_handlers=[GlobHandler(allow_relative=False)],
        location=str(datadir / 'parent_file.yaml')
    )
    assert len(value) == 0
