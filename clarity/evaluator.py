"""Visitor-style evaluator for the Clarity AST."""

from collections.abc import Iterable

from . import ast
from .environment import Environment
from .errors import RuntimeError
from . import semantics
from .runtime import ClarityDict, ClarityFunction

CLARITY_BUILTINS: dict[str, object] = {}


class _LoopSignal(Exception):
    """Internal, non-user-facing signal used to leave a loop body."""


class _BreakSignal(_LoopSignal):
    pass


class _ContinueSignal(_LoopSignal):
    pass


class _ReturnSignal(Exception):
    """Internal signal carrying a function return value."""

    def __init__(self, value: object):
        self.value = value


class Evaluator:
    def __init__(self, environment: Environment | None = None, output=None):
        self.environment = environment or Environment()
        self.output = output or print
        self.loop_depth = 0
        self.function_depth = 0

    def evaluate(self, node):
        method = getattr(self, f"visit_{type(node).__name__}", None)
        if method is None: raise RuntimeError(f"Unsupported syntax: {type(node).__name__}")
        try:
            return method(node)
        except RuntimeError as error:
            raise error.with_span(node.span)

    def visit_ProgramNode(self, node: ast.ProgramNode):
        return self.execute_statements(node.statements)

    def execute_statements(self, statements: list[ast.StatementNode]):
        result = None
        for statement in statements: result = self.evaluate(statement)
        return result

    def execute_block(self, statements: list[ast.StatementNode]):
        """Execute statements in a child scope and always restore the parent scope."""
        previous = self.environment
        self.environment = Environment(previous)
        try:
            return self.execute_statements(statements)
        finally:
            self.environment = previous

    def visit_AssignNode(self, node: ast.AssignNode):
        value = self.evaluate(node.expression)
        self.environment.assign(node.name, value)
        return value

    def visit_AssignIndexNode(self, node: ast.AssignIndexNode):
        target = self.evaluate(node.target)
        index = self.evaluate(node.index)
        value = self.evaluate(node.expression)
        semantics.set_index(target, index, value)
        return value

    def visit_PrintNode(self, node: ast.PrintNode):
        value = self.evaluate(node.expression)
        self.output(semantics.stringify(value))
        return value

    def visit_PushNode(self, node: ast.PushNode):
        target = self.environment.get(node.target)
        if not isinstance(target, list): raise RuntimeError(f"Cannot push to '{node.target}': it is not a list")
        target.append(self.evaluate(node.expression))

    def visit_PopNode(self, node: ast.PopNode):
        target = self.environment.get(node.target)
        if not isinstance(target, list): raise RuntimeError(f"Cannot pop from '{node.target}': it is not a list")
        if not target: raise RuntimeError(f"Cannot pop from '{node.target}': the list is empty")
        return target.pop()

    def visit_BlockNode(self, node: ast.BlockNode):
        return self.execute_block(node.statements)

    def visit_IfNode(self, node: ast.IfNode):
        if semantics.truthy(self.evaluate(node.condition)):
            return self.execute_block(node.then_block.statements)
        if isinstance(node.else_branch, ast.BlockNode):
            return self.execute_block(node.else_branch.statements)
        if isinstance(node.else_branch, ast.IfNode):
            return self.evaluate(node.else_branch)
        return None

    def visit_WhileNode(self, node: ast.WhileNode):
        self.loop_depth += 1
        try:
            while semantics.truthy(self.evaluate(node.condition)):
                try:
                    self.execute_block(node.body.statements)
                except _ContinueSignal:
                    continue
                except _BreakSignal:
                    break
        finally:
            self.loop_depth -= 1

    def visit_ForInNode(self, node: ast.ForInNode):
        iterable = self.evaluate(node.iterable)
        if not isinstance(iterable, (list, str)):
            raise RuntimeError("For-in loops require a list or string")
        self._execute_loop_values(node.variable, list(iterable), node.body)

    def visit_ForRangeNode(self, node: ast.ForRangeNode):
        start = semantics.require_number(self.evaluate(node.start), "Range start")
        end = semantics.require_number(self.evaluate(node.end), "Range end")
        step = 1 if node.step is None else semantics.require_number(self.evaluate(node.step), "Range step")
        if step == 0:
            raise RuntimeError("Range step must not be zero")
        increment = abs(step) if start <= end else -abs(step)
        self._execute_loop_values(node.variable, self._range_values(start, end, increment), node.body)

    def visit_RepeatNode(self, node: ast.RepeatNode):
        raw_count = self.evaluate(node.count)
        count_num = semantics.require_number(raw_count, "Repeat count")
        iterations = int(count_num) if count_num > 0 else 0
        self.loop_depth += 1
        try:
            for _ in range(iterations):
                try:
                    self.execute_block(node.body.statements)
                except _ContinueSignal:
                    continue
                except _BreakSignal:
                    break
        finally:
            self.loop_depth -= 1

    def visit_BreakNode(self, node: ast.BreakNode):
        if self.loop_depth == 0:
            raise RuntimeError("'break' can only be used inside a loop")
        raise _BreakSignal()

    def visit_ContinueNode(self, node: ast.ContinueNode):
        if self.loop_depth == 0:
            raise RuntimeError("'continue' can only be used inside a loop")
        raise _ContinueSignal()

    def visit_FunctionDeclarationNode(self, node: ast.FunctionDeclarationNode):
        function = ClarityFunction(
            node.name,
            tuple(node.parameters),
            node.body,
            self.environment,
            node.span,
        )
        # Define in the current environment so the function can call itself.
        self.environment.define(node.name, function)
        return function

    def visit_ReturnNode(self, node: ast.ReturnNode):
        if self.function_depth == 0:
            raise RuntimeError("'return' can only be used inside a function")
        value = None if node.expression is None else self.evaluate(node.expression)
        raise _ReturnSignal(value)

    def visit_CallNode(self, node: ast.CallNode):
        callee = self.evaluate(node.callee)
        arguments = [self.evaluate(argument) for argument in node.arguments]
        if not isinstance(callee, ClarityFunction):
            raise RuntimeError("Can only call functions")
        if len(arguments) != len(callee.parameters):
            raise RuntimeError(
                f"Function '{callee.display_name()}' expects {len(callee.parameters)} argument(s), got {len(arguments)}"
            )
        return self._call_function(callee, arguments)

    def visit_ExpressionStatementNode(self, node: ast.ExpressionStatementNode):
        return self.evaluate(node.expression)

    def _call_function(self, function: ClarityFunction, arguments: list[object]) -> object:
        caller_environment = self.environment
        caller_loop_depth = self.loop_depth
        call_environment = Environment(function.closure)
        for parameter, argument in zip(function.parameters, arguments, strict=True):
            call_environment.define(parameter.name, argument)

        self.environment = call_environment
        self.loop_depth = 0
        self.function_depth += 1
        try:
            try:
                self.execute_block(function.body.statements)
            except _ReturnSignal as signal:
                return signal.value
            return None
        finally:
            self.function_depth -= 1
            self.loop_depth = caller_loop_depth
            self.environment = caller_environment

    def _execute_loop_values(self, variable: str, values: Iterable[object], body: ast.BlockNode) -> None:
        self.loop_depth += 1
        try:
            for value in values:
                previous = self.environment
                self.environment = Environment(previous)
                self.environment.define(variable, value)
                try:
                    try:
                        self.execute_block(body.statements)
                    except _ContinueSignal:
                        continue
                    except _BreakSignal:
                        break
                finally:
                    self.environment = previous
        finally:
            self.loop_depth -= 1

    @staticmethod
    def _range_values(start: int | float, end: int | float, increment: int | float):
        current = start
        if increment > 0:
            while current <= end:
                yield current
                current += increment
        else:
            while current >= end:
                yield current
                current += increment

    def visit_LiteralNode(self, node: ast.LiteralNode): return node.value
    def visit_IdentifierNode(self, node: ast.IdentifierNode): return self.environment.get(node.name)
    def visit_ListNode(self, node: ast.ListNode): return [self.evaluate(item) for item in node.elements]
    def visit_DictionaryNode(self, node: ast.DictionaryNode):
        d = ClarityDict()
        for key_node, value_node in node.entries:
            key = semantics.validate_dictionary_key(self.evaluate(key_node))
            d[key] = self.evaluate(value_node)
        return d

    def visit_IndexNode(self, node: ast.IndexNode):
        target = self.evaluate(node.target)
        index = self.evaluate(node.index)
        return semantics.get_index(target, index)

    def visit_UnaryOpNode(self, node: ast.UnaryOpNode):
        value = self.evaluate(node.operand)
        if node.operator == "not": return not semantics.truthy(value)
        if node.operator == "-": return -semantics.require_number(value, "unary '-'")
        if node.operator == "+": return +semantics.require_number(value, "unary '+'")
        raise RuntimeError(f"Unknown unary operator: {node.operator}")

    def visit_BinaryOpNode(self, node: ast.BinaryOpNode):
        left = self.evaluate(node.left)
        if node.operator == "and":
            return semantics.truthy(self.evaluate(node.right)) if semantics.truthy(left) else False
        if node.operator == "or":
            return True if semantics.truthy(left) else semantics.truthy(self.evaluate(node.right))
        right = self.evaluate(node.right)
        match node.operator:
            case "+": return semantics.add(left, right)
            case "-": return semantics.subtract(left, right)
            case "*": return semantics.multiply(left, right)
            case "/": return semantics.divide(left, right)
            case "%": return semantics.remainder(left, right)
            case "==": return semantics.equal(left, right)
            case "!=": return not semantics.equal(left, right)
            case ">" | "<" | ">=" | "<=": return semantics.compare(left, right, node.operator)
        raise RuntimeError(f"Unknown binary operator: {node.operator}")
