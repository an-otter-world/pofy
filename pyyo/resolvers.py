"""Resolvers class & utilities.

Resolvers are used when an !include tag is encountered, to load the included
YAML documents.
"""
from abc import abstractmethod
from typing import Union
from yaml import MappingNode
from yaml import SequenceNode


class Resolver:
    """Abstract class used to resolve !include tags."""

    @abstractmethod
    def resolve(self, location) -> Union[MappingNode, SequenceNode]:
        """Resolve the given location.

        Should return a yaml Node, either a sequence or a mapping.
        """
