"""Object field class & utilities."""
from gettext import gettext as _
from inspect import isclass
from typing import AnyStr
from typing import Type

from yaml import MappingNode
from yaml import Node

from pyyo.errors import ErrorCode
from pyyo.loader import load_internal
from pyyo.loading_context import LoadingContext

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
        self._object_class = object_class

    def _load(self, node, context):
        if not isinstance(node, MappingNode):
            context.error(
                node,
                ErrorCode.UNEXPECTED_NODE_TYPE,
                _('Mapping expected')
            )
            return None

        object_class = self._resolve_type(node, context)
        if object_class is None:
            return None

        return load_internal(object_class, node, context)

    def _resolve_type(self, node: Node, context: LoadingContext):
        tag = node.tag
        if not tag.startswith('!type'):
            return self._object_class

        if ':' not in tag:
            context.error(
                node,
                ErrorCode.BAD_TYPE_TAG_FORMAT,
                _TYPE_FORMAT_MSG, tag
            )
            return None

        full_name = tag.split(':')
        if len(full_name) != 2:
            context.error(
                node,
                ErrorCode.BAD_TYPE_TAG_FORMAT,
                _TYPE_FORMAT_MSG, tag
            )
            return None

        full_name_str = full_name[1]
        full_name = full_name_str.split('.')

        if len(full_name) < 2:
            context.error(
                node,
                ErrorCode.BAD_TYPE_TAG_FORMAT,
                _TYPE_FORMAT_MSG, tag
            )
            return None

        module_name = '.'.join(full_name[:-1])
        type_name = full_name[-1]
        return _get_type(node, module_name, type_name, context)


def _get_type(
    node: Node,
    module_name: AnyStr,
    type_name: AnyStr,
    context: LoadingContext
):
    full_name = '{}.{}'.format(module_name, type_name)
    module = __import__(module_name, fromlist=type_name)

    if not hasattr(module, type_name):
        context.error(
            node,
            ErrorCode.TYPE_RESOLVE_ERROR,
            _('Can\'t find python type {}'), full_name
        )
        return None

    resolved_type = getattr(module, type_name)

    if not isclass(resolved_type):
        context.error(
            node,
            ErrorCode.TYPE_RESOLVE_ERROR,
            _('Python type {} is not a class'), full_name
        )
        return None

    return resolved_type
