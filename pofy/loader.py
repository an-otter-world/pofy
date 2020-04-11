"""Pofy deserializing function."""
from gettext import gettext as _
from inspect import isclass
from io import TextIOBase
from pathlib import Path
from typing import IO
from typing import Iterable
from typing import List
from typing import Optional
from typing import Set
from typing import Type
from typing import TypeVar
from typing import Union
from typing import cast

from yaml import compose

from pofy.common import ErrorHandler
from pofy.common import LOADING_FAILED
from pofy.common import LoadResult
from pofy.fields.base_field import BaseField
from pofy.fields.bool_field import BoolField
from pofy.fields.dict_field import DictField
from pofy.fields.float_field import FloatField
from pofy.fields.int_field import IntField
from pofy.fields.list_field import ListField
from pofy.fields.object_field import ObjectField
from pofy.fields.string_field import StringField
from pofy.loading_context import LoadingContext
from pofy.tag_handlers.env_handler import EnvHandler
from pofy.tag_handlers.glob_handler import GlobHandler
from pofy.tag_handlers.if_handler import IfHandler
from pofy.tag_handlers.import_handler import ImportHandler
from pofy.tag_handlers.tag_handler import TagHandler

_ROOT_FIELDS_MAPPING = {
    bool: BoolField(),
    dict: DictField(StringField()),
    float: FloatField(),
    int: IntField(),
    list: ListField(StringField()),
    str: StringField()
}

ObjectType = TypeVar('ObjectType')


def load(
    source: Union[str, IO[str]],
    object_class: Optional[Type[ObjectType]] = None,
    resolve_roots: Optional[Iterable[Path]] = None,
    tag_handlers: Optional[Iterable[TagHandler]] = None,
    error_handler: Optional[ErrorHandler] = None,
    root_field: Optional[BaseField] = None,
    flags: Optional[Set[str]] = None,
) -> LoadResult[ObjectType]:
    """Deserialize a YAML document into an object.

    Args:
        source : Either a string containing YAML, or a stream to a YAML source.
        object_class : Class of the object to create. It will infer the root
                       field to use from this type (Scalar, list, dictionary,
                       or object).
        resolve_roots: Base filesystem paths used to resolve !import and !glob
                       tags.
        tag_handlers : Custom TagHandlers.
        error_handler : Called with arguments (node, error_message) when an
                        error occurs. If it's not specified, a PofyError will
                        be raised when an error occurs.
        root_field: The field to use to load the root node. You can specify a
                    type (list, dict, one of the scalar types or an objec type
                    as cls parameter to get it infered.)
        flags: Flags to define during loading. Those can be used during
               deserialization to customize the loaded objects.

    """
    assert isinstance(source, (str, TextIOBase)), \
        _('source parameter must be a string or Text I/O.')

    all_tag_handlers: List[TagHandler] = []

    if tag_handlers is not None:
        for handler_it in tag_handlers:
            assert isinstance(handler_it, TagHandler), \
                _('tag_handlers items should be subclass of TagHandler')
        all_tag_handlers.extend(tag_handlers)

    all_tag_handlers.append(ImportHandler(resolve_roots))
    all_tag_handlers.append(GlobHandler(resolve_roots))
    all_tag_handlers.append(EnvHandler())
    all_tag_handlers.append(IfHandler())

    if error_handler is not None:
        assert callable(error_handler), \
            _('error_handler must be a callable object.')

    context = LoadingContext(
        error_handler=error_handler,
        tag_handlers=all_tag_handlers,
        flags=flags
    )

    assert isclass(object_class), _('object_class must be a type')
    if root_field is None:
        assert object_class is not None
        root_field = _ROOT_FIELDS_MAPPING.get(object_class)

    if root_field is None:
        assert object_class is not None
        root_field = ObjectField(object_class=object_class)

    node = compose(source) # type: ignore
    node_path = None
    if isinstance(source, TextIOBase) and hasattr(source, 'name'):
        node_path = source.name

    result = context.load(root_field, node, node_path)
    if result is LOADING_FAILED:
        return LOADING_FAILED

    return cast(ObjectType, result)
