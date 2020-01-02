"""Yaml object loading tests."""
from pofy import ListField
from pofy import ObjectField
from pofy import StringField
from pofy import load

from tests.fixtures import load_with_fail_tag


def test_resolve_root_works(datadir):
    """Test giving a path as resolve_root instanciates default tag handlers."""
    class _Owned:
        class Schema:
            """Pyfo fields."""

            test_field = StringField()

    class _Owner:
        class Schema:
            """Pyfo fields."""

            object_field = ObjectField(object_class=_Owned)
            object_list = ListField(
                ObjectField(object_class=_Owned)
            )

    test = load(
        'object_field: !import object.yaml\n',
        _Owner,
        resolve_roots=[datadir]
    )

    assert isinstance(test.object_field, _Owned)
    assert test.object_field.test_field == 'test_value'

    test = load(
        'object_list: !glob glob_directory/*.yaml\n',
        _Owner,
        resolve_roots=[datadir]
    )

    assert len(test.object_list) == 2
    assert isinstance(test.object_list[0], _Owned)
    assert isinstance(test.object_list[1], _Owned)
    assert test.object_list[0].test_field == 'test_value'
    assert test.object_list[1].test_field == 'test_value'


def test_root_field_is_correctly_inferred():
    """Test that the root field is correctly inferred from object_class."""
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


def test_tag_handler_fails_on_root_node_returns_none():
    """Test nothing is deserialized when handling root node fails."""
    assert load_with_fail_tag('!fail some_value', str) is None
