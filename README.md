<h1 align="center">
    <strong>fastapi-dependency</strong>
</h1>
<p align="center">
    <a href="https://github.com/Kludex/fastapi-dependency" target="_blank">
        <img src="https://img.shields.io/github/last-commit/Kludex/fastapi-dependency" alt="Latest Commit">
    </a>
        <img src="https://img.shields.io/github/workflow/status/Kludex/fastapi-dependency/CI">
        <a href="https://github.com/Kludex/fastapi-dependency/actions?workflow=CI" target="_blank">
            <img src="https://img.shields.io/badge/Coverage-100%25-success">
        </a>
    <br />
    <a href="https://pypi.org/project/fastapi-dependency" target="_blank">
        <img src="https://img.shields.io/pypi/v/fastapi-dependency" alt="Package version">
    </a>
    <img src="https://img.shields.io/pypi/pyversions/fastapi-dependency">
    <img src="https://img.shields.io/github/license/Kludex/fastapi-dependency">
</p>

When you use **FastAPI**, you might be tempted to create _sync_ (`def`) dependencies, on which you actually don't perform thread blocking operations.
The thing is that FastAPI will always run your _sync_ dependencies in a thread pool, which is not always necessary.

The goal of this package is to make **explicit** if you want to run a dependency in a thread pool.

## Installation

The package is available on **PyPI**:

```bash
pip install fastapi-dependency
```

## Usage

This package is really small and contains simple functions:

### Depends

> Signature: `Depends(dependency: Callable[..., Any] | None = None, *, use_cache: bool = True, use_thread_pool: bool | None = None)`

This function is a drop-in replacement for `fastapi.Depends` and it has the same signature.
The only difference is that it has an extra parameter: `use_thread_pool`.

If you want to run a dependency in a thread pool, you can set `use_thread_pool` to `True`.

```python
from fastapi import FastAPI
from fastapi_dependency import Depends

app = FastAPI()


def dependency():
    return "Hello World!"

@app.get("/")
def index(message: str = Depends(dependency, use_thread_pool=True)):
    return {"message": message}
```

If you don't set `use_thread_pool` on _sync_ dependencies, it will raise a `RuntimeError`.

### ThreadDepends

> Signature: `ThreadDepends(dependency: Callable[..., Any] | None = None, *, use_cache: bool = True)`

This function is a drop-in replacement for `fastapi.Depends` and it has the same signature.
The only difference is that it will always run the dependency in a thread pool.

```python
from fastapi import FastAPI
from fastapi_dependency import ThreadDepends

app = FastAPI()


def dependency():
    return "Hello World!"

@app.get("/")
def index(message: str = ThreadDepends(dependency)):
    return {"message": message}
```

### ThreadlessDepends

> Signature: `ThreadlessDepends(dependency: Callable[..., Any] | None = None, *, use_cache: bool = True)`

This function is a drop-in replacement for `fastapi.Depends` and it has the same signature.
The only difference is that it will never run the dependency in a thread pool.

```python
from fastapi import FastAPI
from fastapi_dependency import ThreadlessDepends

app = FastAPI()


def dependency():
    return "Hello World!"

@app.get("/")
def index(message: str = ThreadlessDepends(dependency)):
    return {"message": message}
```

### Security

The analogous functions for `fastapi.Security` are:

- `Security`
- `ThreadSecurity`
- `ThreadlessSecurity`

## License

This project is licensed under the terms of the MIT license.
