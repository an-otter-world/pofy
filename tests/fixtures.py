"""Test fixtures & dummy classes."""
from typing import AnyStr
from typing import IO
from typing import List
from typing import Type
from typing import Union

from pofy import ErrorCode
from pofy import Resolver
from pofy import load


def expect_load_error(
    expected_error: ErrorCode,
    object_class: Type,
    source: Union[AnyStr, IO[str]],
    resolvers: List[Resolver] = None
):
    """Load the given object, expecting an error to be raised."""
    error_raised = False

    def _on_error(__, error, ___):
        nonlocal error_raised
        error_raised = True
        assert error == expected_error

    load(
        object_class,
        source,
        error_handler=_on_error,
        resolvers=resolvers
    )
