# 🦆 Quacks

> If it walks like a duck and it quacks like a duck, then it must be a duck

Improved, mypy-compatible duck typing with `Protocol`.

(🚧 work in progress 🚧)

## Why?

PEP544 gave us `Protocol`, a way to define duck typing statically.
In some cases, it's still a bit cumbersome to work with.
This library gives you some much needed niceties.

## Features

### Easy read-only protocols

Defining read-only protocols is great for encouraging immutability and
working with frozen dataclasses. Use the `readonly` decorator:

```python
from quacks import readonly

@readonly
class User(Protocol):
    id: int
    name: str
    is_premium: bool
```

Without this decorator, we'd have to write quite a lot of cruft,
reducing readability:

```python
class User(Protocol):
    @property
    def id(self) -> int: ...
    @property
    def name(self) -> str: ...
    @property
    def is_premium(self) -> bool: ...
```

### Partial protocols

What if you only need part of a protocol?
Imagine we have several functions who use various properties of `User`.
With partial protocols you can reuse a data 'shape' without requiring
all attributes.

(exact syntax TBD)

```python
from quacks import q

def determine_discount(u: User[q.id.is_premium]) -> int:
    ...  # access `id` and `is_premium` attributes

def greet(u: User[q.id.name]) -> None:
    ...  # access `id` and `name` attributes

u: User = ...

determine_discount(u)
greet(u)
```
