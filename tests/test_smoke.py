import inspect

import fastapi_dependency


def test_smoke() -> None:
    assert inspect.ismodule(fastapi_dependency)
