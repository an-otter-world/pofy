"""Pofy deserializing function."""

from gettext import gettext as _
from inspect import getmembers
from inspect import isclass
from typing import AnyStr
from typing import Callable
from typing import IO
from typing import List
from typing import Type
from typing import Union

from yaml import compose
from yaml import MappingNode

from pofy.errors import ErrorCode

from .fields.base_field import BaseField
from .loading_context import LoadingContext
from .resolvers import FileSystemResolver
from .resolvers import Resolver


def load(
    cls: Type,
    source: Union[str, IO[str]],
    resolve_roots: List[AnyStr] = None,
    resolvers: List[Resolver] = None,
    error_handler: Callable = None
) -> object:
    """Deserialize a YAML document into an object.

    Args:
        cls : Class of the object to create.
        source : Either a string containing YAML, or a stream to a YAML source.
        resolve_roots: Base filesystem paths used to resolve !include tags.
                       (will instanciate a pofy.FileSystemResolver for each
                       path if this parameter is not none.)
        resolvers : Custom pofy.Resolvers to use when resolving includes.
        error_handler : Called with arguments (node, error_message) when an
                        error occurs. If it's not specified, a PofyError will
                        be raised when an error occurs.

    """
    node = compose(source)
    all_resolvers = []
    if resolvers is not None:
        all_resolvers.extend(resolvers)

    if resolve_roots is not None:
        file_system_resolvers = [FileSystemResolver(it) for it in resolve_roots]
        all_resolvers.extend(file_system_resolvers)

    context = LoadingContext(
        error_handler=error_handler,
        resolvers=all_resolvers
    )
    with context.push(node):
        return load_internal(cls, context)


def load_internal(object_class: Type, context: LoadingContext):
    """Load given node.

    This function is meant to be used internaly.
    """
    node = context.current_node()

    fields = dict(_get_fields(object_class))

    if not isinstance(node, MappingNode):
        context.error(
            ErrorCode.UNEXPECTED_NODE_TYPE,
            _('Mapping expected')
        )
        return None

    result = object_class()
    set_fields = set()
    for name_node, value_node in node.value:
        with context.push(name_node):
            field_name = name_node.value
            set_fields.add(field_name)
            if field_name not in fields:
                context.error(
                    ErrorCode.FIELD_NOT_DECLARED,
                    _('Field {} is not declared.'), field_name
                )
                continue

        with context.push(value_node):
            field = fields[field_name]
            field_value = field.load(context)
            setattr(result, field_name, field_value)

    for name, field in fields.items():
        if field.required and name not in set_fields:
            context.error(
                ErrorCode.MISSING_REQUIRED_FIELD,
                _('Missing required field {}'), name
            )

    return result


def _is_schema_class(member):
    return isclass(member) and member.__name__ == 'Schema'


def _is_field(member):
    return isinstance(member, BaseField)


def _get_fields(cls):
    for base in cls.__bases__:
        for name, field in _get_fields(base):
            yield (name, field)

    for __, schemaclass in getmembers(cls, _is_schema_class):
        for name, field in getmembers(schemaclass, _is_field):
            yield (name, field)
