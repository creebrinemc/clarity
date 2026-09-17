"""Syntax tree nodes independent from parsing and evaluation."""

from dataclasses import dataclass

from .source import SourceSpan


class Node:
    span: SourceSpan


class StatementNode(Node):
    pass


class ExpressionNode(Node):
    pass

@dataclass(slots=True)
class ProgramNode(Node):
    statements: list[StatementNode]
    span: SourceSpan
@dataclass(slots=True)
class AssignNode(StatementNode):
    name: str
    expression: ExpressionNode
    span: SourceSpan
@dataclass(slots=True)
class PrintNode(StatementNode):
    expression: ExpressionNode
    span: SourceSpan
@dataclass(slots=True)
class PushNode(StatementNode):
    expression: ExpressionNode
    target: str
    span: SourceSpan
@dataclass(slots=True)
class PopNode(StatementNode):
    target: str
    span: SourceSpan
@dataclass(slots=True)
class LiteralNode(ExpressionNode):
    value: object
    span: SourceSpan
@dataclass(slots=True)
class IdentifierNode(ExpressionNode):
    name: str
    span: SourceSpan
@dataclass(slots=True)
class BinaryOpNode(ExpressionNode):
    left: ExpressionNode
    operator: str
    right: ExpressionNode
    span: SourceSpan
@dataclass(slots=True)
class UnaryOpNode(ExpressionNode):
    operator: str
    operand: ExpressionNode
    span: SourceSpan
@dataclass(slots=True)
class ListNode(ExpressionNode):
    elements: list[ExpressionNode]
    span: SourceSpan
@dataclass(slots=True)
class DictionaryNode(ExpressionNode):
    entries: list[tuple[ExpressionNode, ExpressionNode]]
    span: SourceSpan


@dataclass(slots=True)
class BlockNode(StatementNode):
    statements: list[StatementNode]
    span: SourceSpan


@dataclass(slots=True)
class IfNode(StatementNode):
    condition: ExpressionNode
    then_block: BlockNode
    else_branch: BlockNode | "IfNode" | None
    span: SourceSpan


@dataclass(slots=True)
class WhileNode(StatementNode):
    condition: ExpressionNode
    body: BlockNode
    span: SourceSpan


@dataclass(slots=True)
class ForInNode(StatementNode):
    variable: str
    iterable: ExpressionNode
    body: BlockNode
    span: SourceSpan


@dataclass(slots=True)
class ForRangeNode(StatementNode):
    variable: str
    start: ExpressionNode
    end: ExpressionNode
    step: ExpressionNode | None
    body: BlockNode
    span: SourceSpan


@dataclass(slots=True)
class BreakNode(StatementNode):
    span: SourceSpan


@dataclass(slots=True)
class ContinueNode(StatementNode):
    span: SourceSpan


@dataclass(frozen=True, slots=True)
class Parameter:
    name: str
    span: SourceSpan


@dataclass(slots=True)
class FunctionDeclarationNode(StatementNode):
    name: str
    parameters: list[Parameter]
    body: BlockNode
    span: SourceSpan


@dataclass(slots=True)
class ReturnNode(StatementNode):
    expression: ExpressionNode | None
    span: SourceSpan


@dataclass(slots=True)
class CallNode(ExpressionNode):
    callee: ExpressionNode
    arguments: list[ExpressionNode]
    span: SourceSpan


@dataclass(slots=True)
class ExpressionStatementNode(StatementNode):
    expression: ExpressionNode
    span: SourceSpan
