import inspect
from typing import Any, Callable, Optional, Sequence

from fastapi import params
from starlette._utils import is_async_callable


def create_async_wrap(dependency: Callable[..., Any]) -> Callable[..., Any]:
    async def wrap(*args: Any, **kwargs: Any) -> Any:
        return dependency(*args, **kwargs)

    # Pass only parameters from signature to wrap
    dependency_signature = inspect.signature(dependency)
    wrap_signature = inspect.signature(wrap)
    wrap.__signature__ = wrap_signature.replace(  # type: ignore[attr-defined]
        parameters=list(dependency_signature.parameters.values())
    )
    return wrap


def Depends(
    dependency: Optional[Callable[..., Any]] = None,
    *,
    use_cache: bool = True,
    run_in_threadpool: Optional[bool] = None,
) -> Any:
    if dependency is not None and not is_async_callable(dependency):
        if run_in_threadpool is None:
            raise RuntimeError("run_in_threadpool must be set to True or False.")
        if run_in_threadpool is False:
            wrap = create_async_wrap(dependency)
            return params.Depends(dependency=wrap, use_cache=use_cache)
    return params.Depends(dependency=dependency, use_cache=use_cache)


def ThreadDepends(
    dependency: Optional[Callable[..., Any]] = None,
    *,
    use_cache: bool = True,
) -> Any:
    return Depends(dependency=dependency, use_cache=use_cache, run_in_threadpool=True)


def ThreadlessDepends(
    dependency: Optional[Callable[..., Any]] = None,
    *,
    use_cache: bool = True,
) -> Any:
    return Depends(dependency=dependency, use_cache=use_cache, run_in_threadpool=False)


def Security(
    dependency: Optional[Callable[..., Any]] = None,
    *,
    scopes: Optional[Sequence[str]] = None,
    use_cache: bool = True,
    run_in_threadpool: Optional[bool] = None,
) -> Any:
    if dependency is not None and not is_async_callable(dependency):
        if run_in_threadpool is None:
            raise RuntimeError("run_in_threadpool must be set to True or False.")
        if run_in_threadpool is False:
            wrap = create_async_wrap(dependency)
            return params.Security(dependency=wrap, use_cache=use_cache)
    return params.Security(dependency=dependency, scopes=scopes, use_cache=use_cache)


def ThreadSecurity(
    dependency: Optional[Callable[..., Any]] = None,
    *,
    scopes: Optional[Sequence[str]] = None,
    use_cache: bool = True,
) -> Any:
    return Security(
        dependency=dependency,
        scopes=scopes,
        use_cache=use_cache,
        run_in_threadpool=True,
    )


def ThreadlessSecurity(
    dependency: Optional[Callable[..., Any]] = None,
    *,
    scopes: Optional[Sequence[str]] = None,
    use_cache: bool = True,
) -> Any:
    return Security(
        dependency=dependency,
        scopes=scopes,
        use_cache=use_cache,
        run_in_threadpool=False,
    )
