"""Yaml object patching tests."""
from typing import Optional
from typing import List
from typing import Dict

from pofy.fields.list_field import ListField
from pofy.fields.object_field import ObjectField
from pofy.fields.string_field import StringField
from pofy.fields.dict_field import DictField
from pofy.loader import load
from pofy.patch import patch


class _TestSubObject:
    class Schema:
        """Pofy fields."""

        string_field = StringField()

    string_field: Optional[str] = None


class _TestObject:
    class Schema:
        """Pofy fields."""

        object_field = ObjectField(object_class=_TestSubObject)
        list_field = ListField(StringField())
        dict_field = DictField(StringField())

    object_field: Optional[_TestSubObject] = None
    list_field: List[str] = []
    dict_field: Dict[str, str] = {}


def _load_and_patch(original_yaml: str, patch_yaml: str) -> _TestObject:
    result = load(original_yaml, _TestObject)
    assert isinstance(result, _TestObject)
    patch(result, patch_yaml)
    return result


def test_patch_dict_work() -> None:
    """Test patching a dictionary field works."""
    test = _load_and_patch(
        'dict_field: { key: value }',
        'dict_field.key = patched_value'
    )
    assert test.dict_field['key'] == 'patched_value'
