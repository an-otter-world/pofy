"""Yaml object loading tests."""
from io import StringIO

from yaml import compose

from pofy import ErrorCode
from pofy import Resolver
from pofy import load

from tests.fixtures import YamlObject
from tests.fixtures import expect_load_error


class _DummyResolver(Resolver):
    def resolve(self, location):
        if location == 'good_location':
            return compose(StringIO('test_field: test_value'))
        return None


def test_include():
    """Test !include tag uses resolver to find YAML documents to load."""
    test = load(
        YamlObject,
        'object_field: !include good_location',
        resolvers=[_DummyResolver()]
    )
    assert test.object_field.test_field == 'test_value'


def test_include_on_bad_node_raise_error():
    """Test !include tag on a not-scalar node raises an error."""
    expect_load_error(
        ErrorCode.UNEXPECTED_NODE_TYPE,
        YamlObject,
        'object_field: !include [me, is, a, list]'
    )


def test_unresolved_include_raise_error():
    """Test include not found raises an error."""
    expect_load_error(
        ErrorCode.INCLUDE_NOT_FOUND,
        YamlObject,
        'object_field: !include bad_location',
        resolvers=[_DummyResolver()]
    )


def test_field_validation():
    """Test custom field validaton works."""
    expect_load_error(
        ErrorCode.VALIDATION_ERROR,
        YamlObject,
        'validated_field: error_is_always_raised',
    )
