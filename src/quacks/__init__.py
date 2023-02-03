from typing import _GenericAlias  # type: ignore
from typing import TYPE_CHECKING, ClassVar

from typing_extensions import Protocol

# Single-sourcing the version number with poetry:
# https://github.com/python-poetry/poetry/pull/2366#issuecomment-652418094
try:
    __version__ = __import__("importlib.metadata").metadata.version(__name__)
except ModuleNotFoundError:  # pragma: no cover
    __version__ = __import__("importlib_metadata").version(__name__)


__all__ = ["readonly"]


# The logic below allows the mypy plugin to be exposed at root level,
# while also ensuring:
# - mypy doesn't become a runtime dependency
# - mypy itself is not scanned during type checking
if not TYPE_CHECKING:  # pragma: no cover

    def __getattr__(name):
        if name == "plugin":
            from .mypy import plugin

            return plugin
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def readonly(cls: type) -> type:
    """Decorate a :class:`~typing.Protocol` to make it read-only.

    Unlike default protocol attributes, read-only protocols will match
    frozen dataclasses and other immutable types.

    Read-only attributes are already supported in protocols with
    ``@property``, but this is cumbersome to do for many attributes.
    The ``@readonly`` decorator effectively transforms all mutable attributes
    into read-only properties.

    Example
    -------

    .. code-block:: python

        from quacks import readonly

        @readonly
        class User(Protocol):
            id: int
            name: str
            is_premium: bool

        # equivalent to:
        class User(Protocol):
            @property
            def id(self) -> int: ...
            @property
            def name(self) -> str: ...
            @property
            def is_premium(self) -> bool: ...

    Warning
    -------

    Subprotocols and inherited attributes are not supported yet.
    """
    if not _is_a_protocol(cls):
        raise TypeError("Readonly decorator can only be applied to Protocols.")
    elif any(b is not Protocol and _is_a_protocol(b) for b in cls.__bases__):
        raise NotImplementedError("Subprotocols not yet supported.")

    for name, typ in getattr(cls, "__annotations__", {}).items():
        if not _is_classvar(typ):

            @property  # type: ignore
            def prop(self):
                ...  # pragma: no cover

            prop.fget.__name__ = name  # type: ignore
            prop.fget.__annotations__ = {"return": typ}  # type: ignore
            setattr(cls, name, prop)
    return cls


def _is_a_protocol(t: type) -> bool:
    # Only classes *directly* inheriting from Protocol are protocols.
    return Protocol in t.__bases__


def _is_classvar(t: type) -> bool:
    return type(t) is _GenericAlias and t.__origin__ is ClassVar
