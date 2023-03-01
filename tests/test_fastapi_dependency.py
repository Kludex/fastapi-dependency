from typing import Dict

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from fastapi_dependency import (
    Depends,
    Security,
    ThreadDepends,
    ThreadlessDepends,
    ThreadlessSecurity,
    ThreadSecurity,
)


def dependency() -> str:
    return "test"  # pragma: no cover


def test_depends_without_run_in_threadpool() -> None:
    app = FastAPI()

    with pytest.raises(
        RuntimeError, match="run_in_threadpool must be set to True or False."
    ):

        @app.get("/")  # type: ignore[misc]
        def root(depends: str = Depends(dependency)) -> None:
            ...  # pragma: no cover


@pytest.mark.parametrize("run_in_threadpool", [True, False])  # type: ignore[misc]
def test_depends_with_run_in_threadpool(run_in_threadpool: bool) -> None:
    app = FastAPI()

    @app.get("/")  # type: ignore[misc]
    def root(
        depends: str = Depends(dependency, run_in_threadpool=run_in_threadpool)
    ) -> Dict[str, str]:
        return {"depends": depends}

    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"depends": "test"}


def test_thread_depends() -> None:
    app = FastAPI()

    @app.get("/")  # type: ignore[misc]
    def root(depends: str = ThreadDepends(dependency)) -> Dict[str, str]:
        return {"depends": depends}

    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"depends": "test"}


def test_threadless_depends() -> None:
    app = FastAPI()

    @app.get("/")  # type: ignore[misc]
    def root(depends: str = ThreadlessDepends(dependency)) -> Dict[str, str]:
        return {"depends": depends}

    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"depends": "test"}


def test_security_without_run_in_threadpool() -> None:
    app = FastAPI()

    with pytest.raises(
        RuntimeError, match="run_in_threadpool must be set to True or False."
    ):

        @app.get("/")  # type: ignore[misc]
        def root(depends: str = Security(dependency)) -> None:
            ...  # pragma: no cover


def test_security_with_run_in_threadpool() -> None:
    app = FastAPI()

    @app.get("/")  # type: ignore[misc]
    def root(
        depends: str = Security(dependency, run_in_threadpool=True)
    ) -> Dict[str, str]:
        return {"depends": depends}

    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"depends": "test"}


def test_thread_security() -> None:
    app = FastAPI()

    @app.get("/")  # type: ignore[misc]
    def root(depends: str = ThreadSecurity(dependency)) -> Dict[str, str]:
        return {"depends": depends}

    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"depends": "test"}


def test_threadless_security() -> None:
    app = FastAPI()

    @app.get("/")  # type: ignore[misc]
    def root(depends: str = ThreadlessSecurity(dependency)) -> Dict[str, str]:
        return {"depends": "test"}

    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"depends": "test"}
