"""Object field class & utilities."""
from gettext import gettext as _
from inspect import getmembers
from inspect import isclass
from inspect import ismethod
from typing import Any
from typing import Callable
from typing import Dict
from typing import Iterable
from typing import Optional
from typing import Set
from typing import Type
from typing import cast

from pofy.common import ErrorCode
from pofy.common import LOADING_FAILED
from pofy.fields.base_field import BaseField
from pofy.fields.base_field import ValidateCallback
from pofy.fields.string_field import StringField
from pofy.interfaces import ILoadingContext


_TYPE_FORMAT_MSG = _("""\
Type tag should be in the form !type:path.to.Type, got {}""")


class ObjectField(BaseField):
    """Object YAML object field."""

    def __init__(
        self,
        object_class: Type[Any] = object,
        required: bool = False,
        validate: Optional[ValidateCallback] = None,
    ):
        """Initialize object field.

        Arg:
            required: See BaseField constructor.
            validate: See BaseField constructor.
            object_class: The class of the object to create.
            *args, **kwargs: Arguments forwarded to BaseField.

        """
        super().__init__(required=required, validate=validate)
        assert isclass(object_class), \
            _('object_class must be a type')
        self._object_class = object_class

    def _load(self, context: ILoadingContext) -> Any:
        if not context.expect_mapping():
            return LOADING_FAILED

        object_class = self._resolve_type(context)
        if object_class is None:
            return LOADING_FAILED

        return _load(object_class, context)

    def _resolve_type(self, context: ILoadingContext) -> Optional[Type[Any]]:
        node = context.current_node()
        tag = str(node.tag)
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
    context: ILoadingContext
) -> Optional[Type[Any]]:
    full_name = r'{}.{}'.format(module_name, type_name)
    try:
        module = __import__(module_name, fromlist=type_name)
    except ModuleNotFoundError:
        context.error(
            ErrorCode.TYPE_RESOLVE_ERROR,
            _('Can\'t find python module for type {}'), full_name
        )
        return None

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

    return cast(Type[Any], resolved_type)


def _load(object_class: Type[Any], context: ILoadingContext) -> Any:
    fields = _get_fields(object_class, context)

    if fields is None:
        return LOADING_FAILED

    result, set_fields = _load_object(object_class, fields, context)
    if _validate_object(result, fields, set_fields, context):
        return result

    return LOADING_FAILED


def _load_object(
    object_class: Type[Any],
    fields: Dict[str, BaseField],
    context: ILoadingContext
) -> Any:
    node = context.current_node()
    result = object_class()
    set_fields = set()

    for name_node, value_node in node.value:
        field_name = context.load(StringField(), name_node)
        if field_name is LOADING_FAILED:
            continue

        field_name = name_node.value
        set_fields.add(field_name)
        if field_name not in fields:
            context.error(
                ErrorCode.FIELD_NOT_DECLARED,
                _('Field {} is not declared.'), field_name
            )
            continue

        field = fields[field_name]
        field_value = context.load(field, value_node)
        if field_value is LOADING_FAILED:
            continue

        setattr(result, field_name, field_value)

    _post_load(result)

    return (result, set_fields)


def _validate_object(
    obj: Any,
    fields: Dict[str, BaseField],
    set_fields: Set[str],
    context: ILoadingContext
) -> bool:
    object_class = obj.__class__
    valid_object = True
    for name, field in fields.items():
        if field.required and name not in set_fields:
            valid_object = False
            context.error(
                ErrorCode.MISSING_REQUIRED_FIELD,
                _('Missing required field {}'), name
            )

    for validate in _get_methods(object_class, 'validate'):
        if not validate(context, obj):
            valid_object = False

    return valid_object


def _post_load(obj: Any) -> Any:
    object_class = obj.__class__
    for post_load_method in _get_methods(object_class, 'post_load'):
        post_load_method(obj)


def _is_schema_class(member: Any) -> bool:
    return isclass(member) and member.__name__ == 'Schema'


def _is_field(member: Any) -> bool:
    return isinstance(member, BaseField)


def _get_schema_classes(cls: Type[Any]) -> Iterable[Callable[..., Any]]:
    for base in cls.__bases__:
        for schema_class in _get_schema_classes(base):
            yield schema_class

    for __, schema_class in getmembers(cls, _is_schema_class):
        yield schema_class


def _get_fields(cls: Type[Any], context: ILoadingContext) \
        -> Optional[Dict[str, BaseField]]:
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


def _get_methods(cls: Type[Any], method_name: str) \
        -> Iterable[Callable[..., Any]]:
    def _is_validation_method(member: Any) -> bool:
        return ismethod(member) and member.__name__ == method_name

    for base in cls.__bases__:
        for method in _get_methods(base, method_name):
            yield method

    for __, schema_class in getmembers(cls, _is_schema_class):
        for __, method in getmembers(schema_class, _is_validation_method):
            yield method
