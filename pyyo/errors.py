"""Error handling classes & utilities."""
from enum import Enum
from typing import AnyStr

from yaml import Node


class ErrorCode(Enum):
    """Pyyo error codes."""

    BAD_TYPE_TAG_FORMAT = 1
    FIELD_NOT_DECLARED = 2
    MISSING_REQUIRED_FIELD = 3
    UNEXPECTED_NODE_TYPE = 4


class PyyoError(Exception):
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
