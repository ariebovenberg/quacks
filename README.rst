🦆 Quacks
=========

.. image:: https://img.shields.io/pypi/v/quacks.svg
   :target: https://pypi.python.org/pypi/quacks

.. image:: https://img.shields.io/pypi/l/quacks.svg
   :target: https://pypi.python.org/pypi/quacks

.. image:: https://img.shields.io/pypi/pyversions/quacks.svg
   :target: https://pypi.python.org/pypi/quacks

.. image:: https://img.shields.io/readthedocs/quacks.svg
   :target: http://quacks.readthedocs.io/

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black

.. epigraph::

  If it walks like a duck and it quacks like a duck, then it must be a duck

Improved, mypy-compatible duck typing with ``Protocol``.

Why?
----

PEP544 gave us ``Protocol``, a way to define duck typing statically.
In some cases, it's still a bit cumbersome to work with.
This library gives you some much needed niceties.

Features
--------

Easy read-only protocols
^^^^^^^^^^^^^^^^^^^^^^^^

Defining read-only protocols is great for encouraging immutability and
working with frozen dataclasses. Use the ``readonly`` decorator:


.. code-block:: python

    from quacks import readonly

    @readonly
    class User(Protocol):
        id: int
        name: str
        is_premium: bool

Without this decorator, we'd have to write quite a lot of cruft,
reducing readability:


.. code-block:: python

    class User(Protocol):
        @property
        def id(self) -> int: ...
        @property
        def name(self) -> str: ...
        @property

Partial protocols (🚧 work in progress 🚧)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

What if you only need part of a protocol?
Imagine we have several functions who use various properties of ``User``.
With partial protocols you can reuse a data 'shape' without requiring
all attributes.

(exact syntax TBD)

.. code-block:: python

    from quacks import q

    def determine_discount(u: User[q.id.is_premium]) -> int:
        ...  # access `id` and `is_premium` attributes

    def greet(u: User[q.id.name]) -> None:
        ...  # access `id` and `name` attributes

    u: User = ...

    determine_discount(u)
    greet(u)
