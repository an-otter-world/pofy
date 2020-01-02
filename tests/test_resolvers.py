"""Resolvers tests."""
from yaml import MappingNode
from yaml import Node
from yaml import ScalarNode
from yaml import SequenceNode

from pofy import FileSystemResolver


def test_file_system_resolver_resolve_file(datadir):
    """Test file system resolver works with single files."""
    resolver = FileSystemResolver(datadir)
    node = resolver.resolve('object.yaml')
    _check_node(node)


def test_file_system_resolver_resolve_directory(datadir):
    """Test file system resolver works with directories."""
    resolver = FileSystemResolver(datadir)
    node = resolver.resolve('folder/**/*.yaml')
    assert isinstance(node, SequenceNode)

    children = node.value
    assert len(children) == 2
    _check_node(children[0])
    _check_node(children[1])


def _check_node(node: Node):
    assert isinstance(node, MappingNode)
    key_node, value_node = node.value[0]
    assert isinstance(key_node, ScalarNode)
    assert isinstance(value_node, ScalarNode)
    assert key_node.value == 'test_field'
    assert value_node.value == 'test_value'
