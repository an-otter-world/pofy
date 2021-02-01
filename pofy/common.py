"""Pofy common definitions."""
from enum import Enum
from inspect import getmembers
from inspect import isclass
from typing import Any
from typing import Callable
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union
from typing import cast

from yaml import Node


class Undefined:
    """Dummy type representing a failed loading, used for type hints."""


# Unique symbol used to differentiate an error from a valid None return when
# loading a field.
UNDEFINED = Undefined()
ObjectType = TypeVar('ObjectType')
LoadResult = Union[ObjectType, Undefined]
SchemaResolver = Callable[[Type[Any]], Optional[Type[Any]]]


def default_schema_resolver(cls: Type[Any]) -> Optional[Type[Any]]:
    """Return the first inner class named 'Schema' found in given type."""
    def _filter(member: Any) -> bool:
        return isclass(member) and member.__name__ == 'Schema'

    for _, member_it in getmembers(cls, _filter):
        return cast(Type[Any], member_it)

    return None


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

    # Raised when an !import tag can't be resolved.
    IMPORT_NOT_FOUND = 5

    # Raised when a !type tags doesn't resolve to a valid python type.
    TYPE_RESOLVE_ERROR = 6

    # Raised when a value can't be parsed.
    VALUE_ERROR = 7

    # Generic error code for validation errors.
    VALIDATION_ERROR = 8

    # Raised when several handlers matches a tag
    MULTIPLE_MATCHING_HANDLERS = 9

    # Raised when an object schema is incorrect
    SCHEMA_ERROR = 10


ErrorHandler = Callable[[Node, ErrorCode, str], None]


class PofyError(Exception):
    """Exception raised when errors occurs during object loading."""

    def __init__(self, node: Node, message: str):
        """Initialize the error.

        Arg:
            node : The node on which the errTypeor occured.
            code : The error code of the error.
            message : The error description message.

        """
        super().__init__(PofyError._get_message(node, message))
        self.node = node

    @staticmethod
    def _get_message(node: Node, message: str) -> str:
        start = node.start_mark
        file_name = getattr(start, 'name', '<Unkwnown>')
        return '{file}:{line}:{column} : {message}'.format(
            file=file_name,
            line=start.line,
            column=start.column,
            message=message
        )


class BadTypeFormatError(PofyError):
    """Exception type raised for BAD_TYPE_FORMAT error code."""


class FieldNotDeclaredError(PofyError):
    """Exception type raised for FIELD_NOT_DECLARED error code."""


class MissingRequiredFieldError(PofyError):
    """Exception type raised for MISSING_REQUIRED_FIELD error code."""


class UnexpectedNodeTypeError(PofyError):
    """Exception type raised for UNEXPECTED_NODE_TYPE error code."""


class ImportNotFoundError(PofyError):
    """Exception type raised for IMPORT_NOT_FOUND error code."""


class TypeResolveError(PofyError):
    """Exception type raised for TYPE_RESOLVE_ERROR error code."""


class PofyValueError(PofyError):
    """Exception type raised for VALUE_ERROR error code."""


class ValidationError(PofyError):
    """Exception type raised for VALIDATION_ERROR error code."""


class MultipleMatchingHandlersError(PofyError):
    """Exception type raised for MULTIPLE_MATCHING_HANDLER error code."""


class SchemaError(PofyError):
    """Exception type raised for MULTIPLE_MATCHING_HANDLER error code."""


_CODE_TO_EXCEPTION_TYPE_MAPPING = {
    ErrorCode.BAD_TYPE_TAG_FORMAT: BadTypeFormatError,
    ErrorCode.FIELD_NOT_DECLARED: FieldNotDeclaredError,
    ErrorCode.MISSING_REQUIRED_FIELD: MissingRequiredFieldError,
    ErrorCode.UNEXPECTED_NODE_TYPE: UnexpectedNodeTypeError,
    ErrorCode.IMPORT_NOT_FOUND: ImportNotFoundError,
    ErrorCode.TYPE_RESOLVE_ERROR: TypeResolveError,
    ErrorCode.VALUE_ERROR: PofyValueError,
    ErrorCode.VALIDATION_ERROR: ValidationError,
    ErrorCode.MULTIPLE_MATCHING_HANDLERS: MultipleMatchingHandlersError,
    ErrorCode.SCHEMA_ERROR: SchemaError,
}


def get_exception_type(error_code: ErrorCode) -> Type[PofyError]:
    """Get exception type that should be raised for a given error code.

    Args:
        error_code : The error code.

    """
    assert error_code in _CODE_TO_EXCEPTION_TYPE_MAPPING
    return _CODE_TO_EXCEPTION_TYPE_MAPPING[error_code]
