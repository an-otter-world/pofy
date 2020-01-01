"""Object field class & utilities."""
from gettext import gettext as _
from typing import Type

from yaml import MappingNode
from yaml import Node

from pyyo.loader import load_internal
from pyyo.loading_context import LoadingContext

from .base_field import BaseField


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
            context.error(node, _('Expected a mapping'))
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
            context.error(node, _('Bad type tag format : {}'), tag)
            return None

        full_name = tag.split(':')
        if len(full_name) != 2:
            context.error(node, _('Bad type tag format : {}'), tag)
            return None

        full_name = full_name[1].split('.')

        if len(full_name) < 2:
            context.error(node, _('Bad type tag format : {}'), tag)
            return None

        type_module = '.'.join(full_name[:-1])
        type_name = full_name[-1]
        module = __import__(type_module, fromlist=type_name)

        return getattr(module, type_name)
