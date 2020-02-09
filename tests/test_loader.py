"""Yaml object loading tests."""
from io import StringIO
from pathlib import Path
from typing import Any
from typing import Optional
from typing import Type

from yaml import Node

from pofy.common import ErrorCode
from pofy.common import LOADING_FAILED
from pofy.fields.list_field import ListField
from pofy.fields.object_field import ObjectField
from pofy.fields.string_field import StringField
from pofy.interfaces import ILoadingContext
from pofy.loader import load

from tests.helpers import FailTagHandler


def test_resolve_root_works(datadir: Path) -> None:
    """Resolve root should be forwarded to glob and import tag handler."""
    class _Owned:
        class Schema:
            """Pyfo fields."""

            test_field = StringField()

        test_field: Optional[str] = None

    class _Owner:
        class Schema:
            """Pyfo fields."""

            object_field = ObjectField(object_class=_Owned)
            object_list = ListField(
                ObjectField(object_class=_Owned)
            )

        def __init__(self) -> None:
            self.object_field = None
            self.object_list = None

    test = load(
        'object_field: !import object.yaml\n',
        _Owner,
        resolve_roots=[datadir]
    )
    assert isinstance(test, _Owner)
    assert isinstance(test.object_field, _Owned)
    assert test.object_field.test_field == 'test_value'

    test = load(
        'object_list: !glob glob_directory/*.yaml\n',
        _Owner,
        resolve_roots=[datadir]
    )

    assert isinstance(test, _Owner)
    assert len(test.object_list) == 2
    assert isinstance(test.object_list[0], _Owned)
    assert isinstance(test.object_list[1], _Owned)
    assert test.object_list[0].test_field == 'test_value'
    assert test.object_list[1].test_field == 'test_value'


def test_root_field_is_correctly_inferred() -> None:
    """Root field should be inferred from object_class."""
    assert load('on', bool)
    assert load('10', int) == 10
    assert load('10.0', float) == 10.0
    assert load('string_value', str) == 'string_value'
    test_list = load(
        '- item_1\n'
        '- item_2',
        list)

    assert test_list == ['item_1', 'item_2']

    test_dict = load(
        'key_1: value_1\n'
        'key_2: value_2\n',
        dict
    )

    assert test_dict == {'key_1': 'value_1', 'key_2': 'value_2'}


def test_tag_handler_fails_on_root_node_returns_none() -> None:
    """Nothing shoud be deserialized when loading root node fails."""
    result = load(
        '!fail some_value',
        str,
        tag_handlers=[FailTagHandler()]
    )
    assert result is LOADING_FAILED


def test_load_handles_stream(datadir: Path) -> None:
    """It should be correct to give a stream as source parameter for load."""
    with open(datadir / 'object.yaml') as yaml_file:
        test = load(yaml_file, dict)
        assert test == {'test_field': 'test_value'}

    test = load(StringIO('test_field: test_value'), dict)
    assert test == {'test_field': 'test_value'}


def test_load_defines_node_path(datadir: Path) -> None:
    """Calling load with a stream should set the location of the root node."""
    file_path = datadir / 'object.yaml'
    validate_called = False

    class _TestObject:
        class Schema:
            """Pyfo fields."""

            test_field = StringField()

            @classmethod
            def validate(cls: Type[Any], context: ILoadingContext, __: Any) \
                    -> None:
                """Validate that context as correct current_node_path."""
                nonlocal validate_called
                validate_called = True
                assert context.current_location() == str(file_path)

    with open(file_path) as yaml_file:
        load(yaml_file, _TestObject)
        assert validate_called


def test_error_hanlder_is_called() -> None:
    """The given error_handler should be called when defined."""
    handler_called = False

    def _handler(_: Node, __: ErrorCode, ___: str) -> None:
        nonlocal handler_called
        handler_called = True

    load('[a, list]', str, error_handler=_handler)
    assert handler_called
