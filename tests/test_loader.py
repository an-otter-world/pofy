"""Yaml object loading tests."""
from pofy import ListField
from pofy import ObjectField
from pofy import StringField
from pofy import load


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
