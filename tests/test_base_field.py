"""Yaml object loading tests."""
from io import StringIO

from yaml import compose

from pyyo import load
from pyyo import Resolver

from tests.fixtures import YamlObject


class _DummyResolver(Resolver):
    def resolve(self, location):
        assert location == 'some_location'
        return compose(StringIO('test_field: test_value'))


def test_include():
    """Test !include tag uses resolver to find YAML documents to load."""
    test = load(
        YamlObject,
        'object_field: !include some_location',
        resolvers=[_DummyResolver()]
    )
    assert test.object_field.test_field == 'test_value'
