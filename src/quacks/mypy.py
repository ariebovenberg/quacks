from typing import Callable, Optional, Type

from mypy.nodes import AssignmentStmt, NameExpr, Statement, TempNode, Var
from mypy.plugin import ClassDefContext, Plugin
from mypy.types import Instance

READONLY_DECORATOR_NAME = "quacks.readonly"


# this logic is mostly derived from the dataclasses plugin
def make_statement_readonly(c: ClassDefContext, s: Statement) -> None:
    if not (isinstance(s, AssignmentStmt) and s.new_syntax):
        return

    lhs = s.lvalues[0]
    if not isinstance(lhs, NameExpr):
        return

    if not (isinstance(s.rvalue, TempNode) and s.rvalue.no_rhs):
        c.api.msg.fail(
            "@readonly doesn't support default values yet.", context=lhs
        )
        return

    sym = c.cls.info.names.get(lhs.name)
    if sym is None:
        return

    node = sym.node
    assert isinstance(node, Var)
    if node.is_classvar:
        return

    assert isinstance(node.type, Instance)
    node.is_property = True


def make_readonly(c: ClassDefContext) -> None:
    if not c.cls.info.is_protocol:
        c.api.msg.fail(
            "@readonly decorator only supported on protocols.", context=c.cls
        )
    for stmt in c.cls.defs.body:
        make_statement_readonly(c, stmt)


class _QuacksPlugin(Plugin):
    def get_class_decorator_hook(
        self, fullname: str
    ) -> Optional[Callable[[ClassDefContext], None]]:
        if fullname == READONLY_DECORATOR_NAME:
            return make_readonly
        return None


def plugin(version: str) -> Type[Plugin]:
    """Plugin's public API and entrypoint."""
    return _QuacksPlugin
