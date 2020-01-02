"""Pofy deserializing function."""

from typing import AnyStr
from typing import Callable
from typing import IO
from typing import List
from typing import Type
from typing import Union

from yaml import compose

from .fields.base_field import BaseField
from .fields.bool_field import BoolField
from .fields.dict_field import DictField
from .fields.float_field import FloatField
from .fields.int_field import IntField
from .fields.list_field import ListField
from .fields.object_field import ObjectField
from .fields.string_field import StringField
from .loading_context import LoadingContext
from .tag_handlers.glob_handler import GlobHandler
from .tag_handlers.import_handler import ImportHandler
from .tag_handlers.tag_handler import TagHandler

_ROOT_FIELDS_MAPPING = {
    bool: BoolField(),
    dict: DictField(StringField()),
    float: FloatField(),
    int: IntField(),
    list: ListField(StringField()),
    str: StringField()
}


def load(
    source: Union[str, IO[str]],
    object_class: Type = None,
    resolve_roots: List[AnyStr] = None,
    tag_handlers: List[TagHandler] = None,
    error_handler: Callable = None,
    root_field: BaseField = None
) -> object:
    """Deserialize a YAML document into an object.

    Args:
        source : Either a string containing YAML, or a stream to a YAML source.
        object_class : Class of the object to create. It will infer the root
                       field to use from this type (Scalar, list, dictionary,
                       or object).
        resolve_roots: Base filesystem paths used to resolve !include tags.
                       (will instanciate a pofy.FileSystemResolver for each
                       path if this parameter is not none.)
        tag_handlers : Custom pofy.Resolvers to use when resolving includes.
        error_handler : Called with arguments (node, error_message) when an
                        error occurs. If it's not specified, a PofyError will
                        be raised when an error occurs.
        root_field: The field to use to load the root node. You can specify a
                    type (list, dict, one of the scalar types or an objec type
                    as cls parameter to get it infered.)

    """
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

    if root_field is None:
        assert object_class is not None
        root_field = _ROOT_FIELDS_MAPPING.get(object_class)

    if root_field is None:
        assert object_class is not None
        root_field = ObjectField(object_class=object_class)

    node = compose(source)

    with context.load(node) as loaded:
        if not loaded:
            return None

        return root_field.load(context)
