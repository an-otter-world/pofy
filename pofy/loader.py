"""Pofy deserializing function."""

from gettext import gettext as _
from inspect import getmembers
from inspect import isclass
from inspect import ismethod
from typing import Any
from typing import AnyStr
from typing import Callable
from typing import IO
from typing import List
from typing import Set
from typing import Type
from typing import Union

from yaml import compose

from pofy.errors import ErrorCode

from .fields.base_field import BaseField
from .loading_context import LoadingContext
from .tag_handlers.glob_handler import GlobHandler
from .tag_handlers.import_handler import ImportHandler
from .tag_handlers.tag_handler import TagHandler


def load(
    cls: Type,
    source: Union[str, IO[str]],
    resolve_roots: List[AnyStr] = None,
    tag_handlers: List[TagHandler] = None,
    error_handler: Callable = None
) -> object:
    """Deserialize a YAML document into an object.

    Args:
        cls : Class of the object to create.
        source : Either a string containing YAML, or a stream to a YAML source.
        resolve_roots: Base filesystem paths used to resolve !include tags.
                       (will instanciate a pofy.FileSystemResolver for each
                       path if this parameter is not none.)
        tag_handlers : Custom pofy.Resolvers to use when resolving includes.
        error_handler : Called with arguments (node, error_message) when an
                        error occurs. If it's not specified, a PofyError will
                        be raised when an error occurs.

    """
    node = compose(source)
    all_tag_handlers = []
    if tag_handlers is not None:
        all_tag_handlers.extend(tag_handlers)

    if resolve_roots is not None:
        all_tag_handlers.append(ImportHandler(resolve_roots))
        all_tag_handlers.append(GlobHandler(resolve_roots))

    context = LoadingContext(
        error_handler=error_handler,
        tag_handlers=all_tag_handlers
    )
    with context.load(node) as loaded:
        if not loaded:
            return None

        return load_internal(cls, context)


def load_internal(object_class: Type, context: LoadingContext):
    """Load given node.

    This function is meant to be used internaly.
    """
    if not context.expect_mapping():
        return None

    fields = dict(_get_fields(object_class))
    result, set_fields = _load_object(object_class, fields, context)
    if _validate_object(object_class, result, fields, set_fields, context):
        return result

    return None


def _load_object(
    object_class: Type,
    fields: List[BaseField],
    context: LoadingContext
):
    node = context.current_node()
    result = object_class()
    set_fields = set()

    for name_node, value_node in node.value:
        with context.load(name_node) as loaded:
            if not loaded:
                continue

            field_name = name_node.value
            set_fields.add(field_name)
            if field_name not in fields:
                context.error(
                    ErrorCode.FIELD_NOT_DECLARED,
                    _('Field {} is not declared.'), field_name
                )
                continue

        with context.load(value_node) as loaded:
            if not loaded:
                continue

            field = fields[field_name]
            field_value = field.load(context)
            setattr(result, field_name, field_value)

    return (result, set_fields)


def _validate_object(
    object_class: Type,
    obj: Any,
    fields: List[BaseField],
    set_fields: Set[str],
    context: LoadingContext
) -> bool:
    valid_object = True
    for name, field in fields.items():
        if field.required and name not in set_fields:
            valid_object = False
            context.error(
                ErrorCode.MISSING_REQUIRED_FIELD,
                _('Missing required field {}'), name
            )

    for validate in _get_validation_methods(object_class):
        if not validate(context, obj):
            valid_object = False

    return valid_object


def _is_schema_class(member):
    return isclass(member) and member.__name__ == 'Schema'


def _is_field(member):
    return isinstance(member, BaseField)


def _is_validation_method(member):
    return ismethod(member) and member.__name__ == 'validate'


def _get_fields(cls):
    for base in cls.__bases__:
        for name, field in _get_fields(base):
            yield (name, field)

    for __, schemaclass in getmembers(cls, _is_schema_class):
        for name, field in getmembers(schemaclass, _is_field):
            yield (name, field)


def _get_validation_methods(cls):
    for base in cls.__bases__:
        for field in _get_validation_methods(base):
            yield field

    for __, schemaclass in getmembers(cls, _is_schema_class):
        for __, field in getmembers(schemaclass, _is_validation_method):
            yield field
