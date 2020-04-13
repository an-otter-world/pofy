"""If handler tests."""
from pofy.common import UNDEFINED
from pofy.fields.dict_field import DictField
from pofy.fields.list_field import ListField
from pofy.fields.string_field import StringField
from pofy.tag_handlers.if_handler import IfHandler

from tests.helpers import check_load


def test_if_tag_handler() -> None:
    """Env tag should correctly load ifironment variables."""
    result = check_load(
        '!if(FLAG) test_value',
        field=StringField(),
        tag_handlers=[IfHandler()],
        flags={'FLAG'}
    )
    assert result == 'test_value'

    result = check_load(
        '!if(UNDEFINED) test_value',
        field=StringField(),
        tag_handlers=[IfHandler()],
        flags={'FLAG'}
    )
    assert result == UNDEFINED

    result = check_load(
        '!if(FLAG) {key: value}',
        field=DictField(StringField()),
        tag_handlers=[IfHandler()],
        flags={'FLAG'}
    )
    assert result == {'key': 'value'}

    result = check_load(
        '!if(FLAG) [item]',
        field=ListField(StringField()),
        tag_handlers=[IfHandler()],
        flags={'FLAG'}
    )

    assert result == ['item']
