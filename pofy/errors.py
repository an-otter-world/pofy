"""Error handling classes & utilities."""
from enum import Enum
from typing import AnyStr

from yaml import Node


class ErrorCode(Enum):
    """Pofy error codes."""

    # Raised when a !type tag isn't correctly formed.
    BAD_TYPE_TAG_FORMAT = 1

    # Raised when an unknown field is encountered in yaml.
    FIELD_NOT_DECLARED = 2

    # Raised when a required field isn't set in yaml.
    MISSING_REQUIRED_FIELD = 3

    # Raised when a node type isn't the one expected for a field.
    UNEXPECTED_NODE_TYPE = 4

    # Raised when an !include tag can't be resolved.
    INCLUDE_NOT_FOUND = 5

    # Raised when a !type tags doesn't resolve to a valid python type.
    TYPE_RESOLVE_ERROR = 6


class PofyError(Exception):
    """Exception raised when errors occurs during object loading."""

    def __init__(self, node: Node, code: ErrorCode, message: AnyStr):
        """Initialize the error.

        Arg:
            node : The node on which the error occured.
            code : The error code of the error.
            message : The error description message.

        """
        super().__init__()
        self.node = node
        self.code = code
        self.message = message
