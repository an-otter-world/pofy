"""Resolvers class & utilities.

Resolvers are used when an !include tag is encountered, to load the included
YAML documents.
"""
from abc import abstractmethod
from pathlib import Path
from typing import AnyStr
from typing import Union

from yaml import MappingNode
from yaml import SequenceNode
from yaml import compose


class Resolver:
    """Abstract class used to resolve !include tags."""

    @abstractmethod
    def resolve(self, location: AnyStr) -> Union[MappingNode, SequenceNode]:
        """Resolve the given location.

        Return a yaml Node, either a sequence or a mapping.

        Args:
            location: String describing the location of the YAML document to
                      load.

        """


class FileSystemResolver(Resolver):
    """Resolve includes by searching files on the filesystem.

    Allows to use globs with include tag. If multiple files matches, a sequence
    node containing all the deserialized objects will be returned.
    """

    def __init__(self, root: Path):
        """Initialize FileSystemResolver.

        Args:
            root: The root path used when resolving files.

        """
        self._root = root

    def resolve(self, location):
        """See Resolver.resolve for usage."""
        includes = list(self._root.glob(location))
        if len(includes) == 0:
            return None
        if len(includes) == 1:
            with open(includes[0]) as yaml_file:
                return compose(yaml_file)

        nodes = []
        for include in includes:
            with open(include, 'r') as file_it:
                node = compose(file_it)
                nodes.append(node)
        return SequenceNode('', nodes)
