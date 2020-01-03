"""Error handling tests."""
from yaml import Node
from yaml.error import Mark

from pofy import BadTypeFormatError
from pofy import ErrorCode
from pofy import FieldNotDeclaredError
from pofy import ImportNotFoundError
from pofy import MissingRequiredFieldError
from pofy import MultipleMatchingHandlersError
from pofy import PofyError
from pofy import PofyValueError
from pofy import SchemaError
from pofy import TypeResolveError
from pofy import UnexpectedNodeTypeError
from pofy import ValidationError
from pofy import get_exception_type


def test_get_exception_type_is_correct():
    """Test exception type returned by get_exception_type is correct."""
    def _check(code, exception):
        assert get_exception_type(code) == exception

    _check(ErrorCode.BAD_TYPE_TAG_FORMAT, BadTypeFormatError)
    _check(ErrorCode.FIELD_NOT_DECLARED, FieldNotDeclaredError)
    _check(ErrorCode.MISSING_REQUIRED_FIELD, MissingRequiredFieldError)
    _check(ErrorCode.UNEXPECTED_NODE_TYPE, UnexpectedNodeTypeError)
    _check(ErrorCode.IMPORT_NOT_FOUND, ImportNotFoundError)
    _check(ErrorCode.TYPE_RESOLVE_ERROR, TypeResolveError)
    _check(ErrorCode.VALUE_ERROR, PofyValueError)
    _check(ErrorCode.VALIDATION_ERROR, ValidationError)
    _check(ErrorCode.MULTIPLE_MATCHING_HANDLERS, MultipleMatchingHandlersError)
    _check(ErrorCode.SCHEMA_ERROR, SchemaError)


def test_exception_format():
    """Test exception __str__ method gives usefull informations."""
    node = Node(
        'tag',
        'value',
        Mark('file_name', 0, 10, 42, None, None),
        Mark('file_name', 0, 12, 32, None, None)
    )

    message = 'Error message'
    error = PofyError(node, message)

    location_string = '{}:{}:{}'.format('file_name', 10, 42)

    error_string = str(error)
    assert location_string in error_string
    assert message in error_string
