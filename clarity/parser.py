"""Recursive-descent parser for Clarity 0.4."""

from . import ast
from .errors import ParserError
from .tokens import Token, TokenType


class Parser:
    def __init__(self, tokens: list[Token]): self.tokens, self.current = tokens, 0

    def parse(self) -> ast.ProgramNode:
        statements = []
        start = self._peek().span
        self._skip_newlines()
        while not self._check(TokenType.EOF):
            if self._check(TokenType.RIGHT_BRACE):
                self._error(self._peek(), "Unexpected '}' outside a block")
            statements.append(self._statement())
            self._finish_statement()
        span = statements[0].span.cover(statements[-1].span) if statements else start.cover(self._peek().span)
        return ast.ProgramNode(statements, span)

    def _statement(self) -> ast.StatementNode:
        if self._match(TokenType.LEFT_BRACE): return self._block()
        if self._match_keyword("set"):
            start = self._previous()
            target = self._postfix()
            self._consume_keyword("to", "Expected 'to' after variable name")
            expression = self._expression()
            if isinstance(target, ast.IdentifierNode):
                return ast.AssignNode(target.name, expression, start.span.cover(expression.span))
            if isinstance(target, ast.IndexNode):
                return ast.AssignIndexNode(target.target, target.index, expression, start.span.cover(expression.span))
            self._error(target, "Expected variable name or index target after 'set'")
        if self._match_keyword("say"):
            start = self._previous()
            expression = self._expression()
            return ast.PrintNode(expression, start.span.cover(expression.span))
        if self._match_keyword("push"):
            start = self._previous()
            value = self._expression()
            self._consume_keyword("to", "Expected 'to' after value to push")
            target = self._consume(TokenType.IDENTIFIER, "Expected list variable after 'to'")
            return ast.PushNode(value, target.value, start.span.cover(target.span))
        if self._match_keyword("pop"):
            start = self._previous()
            self._consume_keyword("from", "Expected 'from' after 'pop'")
            target = self._consume(TokenType.IDENTIFIER, "Expected list variable after 'from'")
            return ast.PopNode(target.value, start.span.cover(target.span))
        if self._match_keyword("if"):
            return self._if_statement(self._previous())
        if self._match_keyword("while"):
            start = self._previous()
            condition = self._expression()
            body = self._consume_block("Expected '{' after while condition")
            return ast.WhileNode(condition, body, start.span.cover(body.span))
        if self._match_keyword("for"):
            return self._for_statement(self._previous())
        if self._match_keyword("repeat"):
            return self._repeat_statement(self._previous())
        if self._match_keyword("break"):
            return ast.BreakNode(self._previous().span)
        if self._match_keyword("continue"):
            return ast.ContinueNode(self._previous().span)
        if self._match_keyword("function"):
            return self._function_declaration(self._previous())
        if self._match_keyword("return"):
            return self._return_statement(self._previous())
        start = self._peek()
        start_index = self.current
        try:
            expression = self._expression()
        except ParserError:
            if self.current == start_index:
                self._error(start, "Expected a statement")
            raise
        if not isinstance(expression, ast.CallNode):
            self._error(start, "Expected a statement")
        return ast.ExpressionStatementNode(expression, expression.span)

    def _repeat_statement(self, start: Token) -> ast.RepeatNode:
        count = self._expression()
        self._consume_keyword("times", "Expected 'times' after repeat count")
        body = self._consume_block("Expected '{' after repeat statement")
        return ast.RepeatNode(count, body, start.span.cover(body.span))

    def _function_declaration(self, start: Token) -> ast.FunctionDeclarationNode:
        name = self._consume(TokenType.IDENTIFIER, "Expected function name after 'function'")
        parameters: list[ast.Parameter] = []
        seen_names: set[str] = set()
        if self._match_keyword("taking"):
            parameter = self._consume(TokenType.IDENTIFIER, "Expected parameter name after 'taking'")
            parameters.append(self._parameter(parameter, seen_names))
            while self._match_keyword("and"):
                parameter = self._consume(TokenType.IDENTIFIER, "Expected parameter name after 'and'")
                parameters.append(self._parameter(parameter, seen_names))
        body = self._consume_block("Expected '{' after function declaration")
        return ast.FunctionDeclarationNode(name.value, parameters, body, start.span.cover(body.span))

    def _parameter(self, token: Token, seen_names: set[str]) -> ast.Parameter:
        if token.value in seen_names:
            self._error(token, f"Duplicate parameter name: {token.value}")
        seen_names.add(token.value)
        return ast.Parameter(token.value, token.span)

    def _return_statement(self, start: Token) -> ast.ReturnNode:
        if self._check(TokenType.NEWLINE) or self._check(TokenType.RIGHT_BRACE) or self._check(TokenType.EOF):
            return ast.ReturnNode(None, start.span)
        expression = self._expression()
        return ast.ReturnNode(expression, start.span.cover(expression.span))

    def _if_statement(self, start: Token) -> ast.IfNode:
        condition = self._expression()
        then_block = self._consume_block("Expected '{' after if condition")
        else_branch = None
        if self._match_else_after_block():
            else_token = self._previous()
            if self._match_keyword("if"):
                else_branch = self._if_statement(self._previous())
            elif self._match(TokenType.LEFT_BRACE):
                else_branch = self._block()
            else:
                self._error(self._peek(), "Expected 'if' or '{' after 'else'")
        end_span = else_branch.span if else_branch else then_block.span
        return ast.IfNode(condition, then_block, else_branch, start.span.cover(end_span))

    def _for_statement(self, start: Token) -> ast.StatementNode:
        self._match_keyword("each")
        variable = self._consume(TokenType.IDENTIFIER, "Expected loop variable after 'for'")
        if self._match_keyword("in"):
            iterable = self._expression()
            body = self._consume_block("Expected '{' after for-in iterable")
            return ast.ForInNode(variable.value, iterable, body, start.span.cover(body.span))
        if self._match_keyword("from"):
            range_start = self._expression()
            self._consume_keyword("to", "Expected 'to' after range start")
            range_end = self._expression()
            step = None
            if self._match_keyword("step"):
                step = self._expression()
            body = self._consume_block("Expected '{' after range loop")
            return ast.ForRangeNode(variable.value, range_start, range_end, step, body, start.span.cover(body.span))
        self._error(self._peek(), "Expected 'in' or 'from' after loop variable")

    def _consume_block(self, message: str) -> ast.BlockNode:
        if self._match(TokenType.LEFT_BRACE): return self._block()
        self._error(self._peek(), message)

    def _block(self) -> ast.BlockNode:
        opening = self._previous()
        statements: list[ast.StatementNode] = []
        self._skip_newlines()
        while not self._check(TokenType.RIGHT_BRACE):
            if self._check(TokenType.EOF):
                self._error(self._peek(), "Expected '}' to close block")
            statements.append(self._statement())
            self._finish_statement(in_block=True)
        closing = self._consume(TokenType.RIGHT_BRACE, "Expected '}' to close block")
        return ast.BlockNode(statements, opening.span.cover(closing.span))

    def _match_else_after_block(self) -> bool:
        if self._match_keyword("else"): return True
        if not self._check(TokenType.NEWLINE): return False
        saved = self.current
        self._skip_newlines()
        if self._match_keyword("else"): return True
        self.current = saved
        return False

    def _finish_statement(self, in_block: bool = False) -> None:
        if self._match(TokenType.NEWLINE):
            self._skip_newlines()
            return
        if self._check(TokenType.EOF) or (in_block and self._check(TokenType.RIGHT_BRACE)):
            return
        self._error(self._peek(), "Expected a newline after statement")

    def _expression(self): return self._logical_or()
    def _logical_or(self): return self._binary(self._logical_and, lambda: self._match_keyword("or"))
    def _logical_and(self): return self._binary(self._equality, lambda: self._match_keyword("and"))

    def _equality(self):
        node = self._comparison()
        while True:
            op = self._match_equality_op()
            if op is None: break
            right = self._comparison()
            node = ast.BinaryOpNode(node, op, right, node.span.cover(right.span))
        return node

    def _comparison(self):
        node = self._term()
        while True:
            op = self._match_comparison_op()
            if op is None: break
            right = self._term()
            node = ast.BinaryOpNode(node, op, right, node.span.cover(right.span))
        return node

    def _match_equality_op(self) -> str | None:
        if self._match_operator("==", "!="):
            return self._previous().value
        if self._check_keyword("is"):
            if self._check_next_keyword(1, "equal"):
                self._advance()  # is
                self._advance()  # equal
                self._consume_keyword("to", "Expected 'to' after 'is equal'")
                return "=="
            if self._check_next_keyword(1, "not") and self._check_next_keyword(2, "equal"):
                self._advance()  # is
                self._advance()  # not
                self._advance()  # equal
                self._consume_keyword("to", "Expected 'to' after 'is not equal'")
                return "!="
        return None

    def _match_comparison_op(self) -> str | None:
        if self._match_operator(">", "<", ">=", "<="):
            return self._previous().value
        if self._check_keyword("is"):
            if self._check_next_keyword(1, "greater"):
                self._advance()  # is
                self._advance()  # greater
                self._consume_keyword("than", "Expected 'than' after 'is greater'")
                return ">"
            if self._check_next_keyword(1, "less"):
                self._advance()  # is
                self._advance()  # less
                self._consume_keyword("than", "Expected 'than' after 'is less'")
                return "<"
            if self._check_next_keyword(1, "at"):
                self._advance()  # is
                self._advance()  # at
                if self._match_keyword("least"):
                    return ">="
                if self._match_keyword("most"):
                    return "<="
                self._error(self._peek(), "Expected 'least' or 'most' after 'is at'")
        return None

    def _term(self): return self._binary(self._factor, lambda: self._match_operator("+", "-"))
    def _factor(self): return self._binary(self._unary, lambda: self._match_operator("*", "/", "%"))

    def _binary(self, next_level, matcher):
        node = next_level()
        while matcher():
            operator = self._previous().value
            right = next_level()
            node = ast.BinaryOpNode(node, operator, right, node.span.cover(right.span))
        return node

    def _unary(self):
        if self._match_operator("-", "+") or self._match_keyword("not"):
            operator = self._previous()
            operand = self._unary()
            return ast.UnaryOpNode(operator.value, operand, operator.span.cover(operand.span))
        return self._postfix()

    def _postfix(self):
        expression = self._primary()
        while True:
            if self._match(TokenType.LEFT_PAREN):
                arguments = []
                if not self._check(TokenType.RIGHT_PAREN):
                    while True:
                        arguments.append(self._expression())
                        if not self._match(TokenType.COMMA): break
                closing = self._consume(TokenType.RIGHT_PAREN, "Expected ')' after function arguments")
                expression = ast.CallNode(expression, arguments, expression.span.cover(closing.span))
            elif self._match(TokenType.LEFT_BRACKET):
                index = self._expression()
                closing = self._consume(TokenType.RIGHT_BRACKET, "Expected ']' after index")
                expression = ast.IndexNode(expression, index, expression.span.cover(closing.span))
            else:
                break
        return expression

    def _primary(self):
        if self._match(TokenType.NUMBER, TokenType.STRING, TokenType.BOOLEAN, TokenType.NULL):
            token = self._previous()
            return ast.LiteralNode(token.value, token.span)
        if self._match(TokenType.IDENTIFIER):
            token = self._previous()
            return ast.IdentifierNode(token.value, token.span)
        if self._match(TokenType.LEFT_PAREN):
            opening = self._previous()
            expr = self._expression()
            closing = self._consume(TokenType.RIGHT_PAREN, "Expected ')' after expression")
            expr.span = opening.span.cover(closing.span)
            return expr
        if self._match(TokenType.LEFT_BRACKET): return self._list()
        if self._match(TokenType.LEFT_BRACE): return self._dictionary()
        self._error(self._peek(), "Expected an expression")

    def _list(self):
        opening = self._previous()
        elements = []
        self._skip_newlines()
        if not self._check(TokenType.RIGHT_BRACKET):
            while True:
                self._skip_newlines()
                elements.append(self._expression())
                self._skip_newlines()
                if not self._match(TokenType.COMMA): break
                self._skip_newlines()
        self._skip_newlines()
        closing = self._consume(TokenType.RIGHT_BRACKET, "Expected ']' after list")
        return ast.ListNode(elements, opening.span.cover(closing.span))

    def _dictionary(self):
        opening = self._previous()
        entries = []
        self._skip_newlines()
        if not self._check(TokenType.RIGHT_BRACE):
            while True:
                self._skip_newlines()
                if self._match(TokenType.IDENTIFIER):
                    token = self._previous()
                    key = ast.LiteralNode(token.value, token.span)
                else:
                    key = self._expression()
                self._consume(TokenType.COLON, "Expected ':' after dictionary key")
                self._skip_newlines()
                value = self._expression()
                entries.append((key, value))
                self._skip_newlines()
                if not self._match(TokenType.COMMA): break
                self._skip_newlines()
        self._skip_newlines()
        closing = self._consume(TokenType.RIGHT_BRACE, "Expected '}' after dictionary")
        return ast.DictionaryNode(entries, opening.span.cover(closing.span))

    def _match(self, *types):
        if self._peek().type in types: self._advance(); return True
        return False
    def _match_keyword(self, value): return self._match_value(TokenType.KEYWORD, value)
    def _match_operator(self, *values): return any(self._match_value(TokenType.OPERATOR, value) for value in values)
    def _match_value(self, kind, value):
        if self._check(kind) and self._peek().value == value: self._advance(); return True
        return False
    def _check_keyword(self, value: str) -> bool:
        return self._check(TokenType.KEYWORD) and self._peek().value == value
    def _check_next_keyword(self, offset: int, value: str) -> bool:
        idx = self.current + offset
        if idx < len(self.tokens):
            token = self.tokens[idx]
            return token.type == TokenType.KEYWORD and token.value == value
        return False
    def _consume(self, kind, message):
        if self._check(kind): return self._advance()
        self._error(self._peek(), message)
    def _consume_keyword(self, value, message):
        if self._match_keyword(value): return self._previous()
        self._error(self._peek(), message)
    def _check(self, kind): return self._peek().type == kind
    def _advance(self):
        if not self._check(TokenType.EOF): self.current += 1
        return self._previous()
    def _peek(self): return self.tokens[self.current]
    def _previous(self): return self.tokens[self.current - 1]
    def _skip_newlines(self):
        while self._match(TokenType.NEWLINE): pass
    def _error(self, token, message): raise ParserError(message, token.span)
