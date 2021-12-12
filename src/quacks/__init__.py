from typing_extensions import Protocol

# Single-sourcing the version number with poetry:
# https://github.com/python-poetry/poetry/pull/2366#issuecomment-652418094
try:
    __version__ = __import__("importlib.metadata").metadata.version(__name__)
except ModuleNotFoundError:  # pragma: no cover
    __version__ = __import__("importlib_metadata").version(__name__)


def readonly(cls: type) -> type:
    """Decorate a :class:`~typing.Protocol` to make it readonly.

    Unlike default protocol attributes, readonly protocols will match
    frozen dataclasses and other immutable types.

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

    Warning
    -------

    Subprotocols and inherited attributes are not supported yet.
    """
    if Protocol not in cls.__bases__:
        raise TypeError("Readonly decorator can only be applied to Protocols.")
    elif any(
        b is not Protocol and Protocol in b.__bases__
        for b in cls.__bases__
    ):
        raise NotImplementedError("Subprotocols not yet supported.")
    return cls
