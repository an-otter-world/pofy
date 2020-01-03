"""Object field class & utilities."""
from gettext import gettext as _
from inspect import getmembers
from inspect import isclass
from inspect import ismethod
from typing import Any
from typing import Dict
from typing import Optional
from typing import Set
from typing import Type

from pofy.errors import ErrorCode
from pofy.loading_context import LoadingContext

from .base_field import BaseField

_TYPE_FORMAT_MSG = _("""\
Type tag should be in the form !type:path.to.Type, got {}""")


class ObjectField(BaseField):
    """Object YAML object field."""

    def __init__(self, *args, object_class: Type = object, **kwargs):
        """Initialize object field.

        Arg:
            object_class: The class of the object to create.
            *args, **kwargs: Arguments forwarded to BaseField.

        """
        super().__init__(*args, **kwargs)
        assert isclass(object_class), \
            _('object_class must be a type')
        self._object_class = object_class

    def _load(self, context: LoadingContext):
        if not context.expect_mapping():
            return None

        object_class = self._resolve_type(context)
        if object_class is None:
            return None

        return _load(object_class, context)

    def _resolve_type(self, context: LoadingContext):
        node = context.current_node()
        tag = node.tag
        if not tag.startswith('!type'):
            return self._object_class

        if ':' not in tag:
            context.error(
                ErrorCode.BAD_TYPE_TAG_FORMAT,
                _TYPE_FORMAT_MSG, tag
            )
            return None

        full_name = tag.split(':')
        if len(full_name) != 2:
            context.error(
                ErrorCode.BAD_TYPE_TAG_FORMAT,
                _TYPE_FORMAT_MSG, tag
            )
            return None

        full_name_str = full_name[1]
        full_name = full_name_str.split('.')

        if len(full_name) < 2:
            context.error(
                ErrorCode.BAD_TYPE_TAG_FORMAT,
                _TYPE_FORMAT_MSG, tag
            )
            return None

        module_name = '.'.join(full_name[:-1])
        type_name = full_name[-1]
        return _get_type(module_name, type_name, context)


def _get_type(
    module_name: str,
    type_name: str,
    context: LoadingContext
):
    full_name = r'{}.{}'.format(module_name, type_name)
    module = __import__(module_name, fromlist=type_name)

    if not hasattr(module, type_name):
        context.error(
            ErrorCode.TYPE_RESOLVE_ERROR,
            _('Can\'t find python type {}'), full_name
        )
        return None

    resolved_type = getattr(module, type_name)

    if not isclass(resolved_type):
        context.error(
            ErrorCode.TYPE_RESOLVE_ERROR,
            _('Python type {} is not a class'), full_name
        )
        return None

    return resolved_type


def _load(object_class: Type, context: LoadingContext):
    fields = _get_fields(object_class, context)

    if fields is None:
        return None

    result, set_fields = _load_object(object_class, fields, context)
    if _validate_object(object_class, result, fields, set_fields, context):
        return result

    return None


def _load_object(
    object_class: Type,
    fields: Dict[str, BaseField],
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
    fields: Dict[str, BaseField],
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


def _get_schema_classes(cls):
    for base in cls.__bases__:
        for schema_class in _get_schema_classes(base):
            yield schema_class

    for __, schema_class in getmembers(cls, _is_schema_class):
        yield schema_class


def _get_fields(cls, context: LoadingContext) -> Optional[Dict[str, BaseField]]:
    schema_classes = list(_get_schema_classes(cls))

    if len(schema_classes) == 0:
        context.error(
            ErrorCode.SCHEMA_ERROR,
            _('No Schema class found for type {}, check that your schema is '
              'correctly configured.'),
            cls.__name__
        )
        return None

    fields = {}
    for schema_it in schema_classes:
        for name, field in getmembers(schema_it, _is_field):
            fields[name] = field

    return fields


def _get_validation_methods(cls):
    for base in cls.__bases__:
        for field in _get_validation_methods(base):
            yield field

    for __, schemaclass in getmembers(cls, _is_schema_class):
        for __, field in getmembers(schemaclass, _is_validation_method):
            yield field
