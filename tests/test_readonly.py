from typing import ClassVar

import pytest
from typing_extensions import Protocol

from quacks import readonly


def test_empty():
    class Z(Protocol):
        ...

    @readonly
    class A(Protocol):
        ...

    assert A.__dict__.keys() >= Z.__dict__.keys()


def test_only_protocols_accepted():
    with pytest.raises(TypeError, match="Protocol"):

        @readonly
        class C:  # type: ignore
            ...


def test_protocol_implementation_not_accepted():

    with pytest.raises(TypeError, match="Protocol"):

        class A(Protocol):
            ...

        @readonly
        class C(A):  # type: ignore
            ...


def test_subprotocols_not_supported():
    with pytest.raises(NotImplementedError, match="Subprotocol"):

        class A(Protocol):
            ...

        @readonly
        class C(A, Protocol):
            ...


def test_no_mutable_fields():
    @readonly
    class B(Protocol):
        @property
        def myprop(self) -> int:
            return 8

        def zzz(self, k: int) -> str:
            return k * "z"

    assert isinstance(B.myprop, property)


def test_freezes_attributes_into_properties():
    @readonly
    class A(Protocol):
        a: float
        b: int

        k: ClassVar[str]

        @property
        def myprop(self) -> int:
            return 8

        def zzz(self, k: int) -> str:
            return k * "z"

    assert isinstance(A.a, property)
    assert A.a.fget.__annotations__ == {"return": float}
    assert A.a.fget.__name__ == "a"  # type: ignore
    assert isinstance(A.b, property)
    assert A.b.fget.__annotations__ == {"return": int}
    assert A.b.fget.__name__ == "b"  # type: ignore
    assert not hasattr(A, "k")
