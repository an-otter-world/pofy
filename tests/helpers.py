"""Test helpers."""
from typing import Any
from typing import IO
from typing import List
from typing import Type
from typing import Union

from yaml import Node
from yaml import compose

from pofy import BaseField
from pofy import ErrorCode
from pofy import LOADING_FAILED
from pofy import LoadingContext
from pofy import ObjectField
from pofy import TagHandler


def check_field(
    object_class: Type,
    field_name: str,
    field_value: str,
    expected_value: Any
):
    """Check a field correctly loads the given YAML value."""
    result = check_load(
        '{}: {}'.format(field_name, field_value),
        object_class
    )

    assert getattr(result, field_name) == expected_value


def check_field_error(
    object_class: Type,
    field_name: str,
    field_value: str,
    expected_error: ErrorCode,
):
    """Check that loading emits the given error and doesn't set the field."""
    result = check_load(
        '{}: {}'.format(field_name, field_value),
        object_class,
        expected_error=expected_error,
    )
    assert not hasattr(result, field_value)


def check_load(
    source: Union[str, IO[str]],
    object_class: Type[Any] = None,
    expected_error: ErrorCode = None,
    field: BaseField = None,
    location: str = None,
    tag_handlers: List[TagHandler] = None,
):
    """Load a yaml document, given the specified parameters."""
    if tag_handlers is None:
        tag_handlers = []

    tag_handlers.append(FailTagHandler())

    handler_called = False

    def _handler(__: Node, code: ErrorCode, ___: str):
        nonlocal handler_called
        handler_called = True
        assert expected_error is not None
        assert code == expected_error

    context = LoadingContext(_handler, tag_handlers)
    node = compose(source)

    if field is None:
        assert object_class is not None
        field = ObjectField(object_class=object_class)

    result = context.load(field, node, str(location))

    if expected_error is not None:
        assert handler_called

    return result


class FailTagHandler(TagHandler):
    """Tag handlers that returns LOADING_FAILED."""

    tag_pattern = '^fail$'

    def load(self, __, ___):
        return LOADING_FAILED
