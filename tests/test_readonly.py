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

    assert len(A.__dict__) == len(Z.__dict__)


def test_only_protocols_accepted():
    with pytest.raises(TypeError, match="Protocol"):

        @readonly
        class C:
            ...


def test_protocol_implementation_not_accepted():

    with pytest.raises(TypeError, match="Protocol"):

        class A(Protocol):
            ...

        @readonly
        class C(A):
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

    len(B.__dict__) == 13


def test_freezes_attributes():
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
    assert isinstance(A.b, property)
    assert not hasattr(A, 'k')
