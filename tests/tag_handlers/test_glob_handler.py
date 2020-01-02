"""Glob handler tests."""
from yaml import SequenceNode
from yaml import ScalarNode

from pofy import ErrorCode
from pofy import GlobHandler

from tests.fixtures import mock_loading_context


def test_bad_node_for_glob_raises():
    """Test glob tag on a not-scalar node raise an error."""
    with mock_loading_context(
        node=SequenceNode('!glob', '', None, None),
        expected_error=ErrorCode.UNEXPECTED_NODE_TYPE,
        tag_handlers=[GlobHandler([])]
    ):
        pass


def test_glob_resolves_correctly(datadir):
    """Test glob resolves correctly files."""
    handler = GlobHandler([datadir])
    with mock_loading_context(
        node=ScalarNode('!glob', 'folder/**/*', None, None),
        tag_handlers=[handler]
    ) as context:
        node = context.current_node()
        assert isinstance(node, SequenceNode)
        assert len(node.value) == 2
        assert node.value[0].value in ['file2_content', 'file3_content']
        assert node.value[1].value in ['file2_content', 'file3_content']


def test_glob_raise_error_on_yaml_load_failure(datadir):
    """Test glob raises a VALUE_ERROR if a file can't be deserialized."""
    handler = GlobHandler([datadir])
    with mock_loading_context(
        node=ScalarNode('!glob', '**/*', None, None),
        expected_error=ErrorCode.VALUE_ERROR,
        tag_handlers=[handler]
    ):
        pass
