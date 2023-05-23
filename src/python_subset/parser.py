#!/usr/bin/env python3
from dataclasses import dataclass
from typing import Union
from lexer import *
from icecream import ic

# Grammar:
# block = statement+
# statement = assignment_statement
#           | expression
# expression = term (("+"|"-") term)*
# term = factor (("*"|"/") factor)*
# factor = ID | Number | "(" expression ")"

@dataclass
class Variable:
    name: str

@dataclass
class Number:
    value: str

@dataclass
class Factor:
    op: Union[str, None]
    value: Union[Variable, Number, 'Expression']

@dataclass
class Term:
    op: Union[str, None]
    factors: list[Factor]

@dataclass
class Expression:
    terms: list[Term]

@dataclass
class AssignmentStatement:
    var: Variable
    expr: Expression

@dataclass
class Condition:
    expr1: Expression
    op: str
    expr2: Expression

@dataclass
class Block:
    statements: list[Union[Expression, AssignmentStatement]]


class Parser:
    # self.tok holds the previously consumed token
    # self.token holds the list of tokens,

    def next_tok(self):
        '''Returns the next token without consuming it.'''
        return self.tokens[0]


    def consume_tok(self):
        '''Consumes the next token and returns it.'''
        return self.tokens.pop(0)


    def tokens_left(self):
        '''Returns the number of tokens left to consume.'''
        return len(self.tokens)


    def accept(self, toktype, values=()):
        '''
        If next token is toktype, consumes it and returns it,
        otherwise don't consume it and return False.
        '''
        if self.tokens_left() and self.next_tok().type == toktype \
            and (not values or self.next_tok().value in values):
            self.tok = self.consume_tok()
            return True
        return False


    def expect(self, toktype, values=()):
        '''
        If next token is not toktype, raise error, otherwise return the token.
        '''
        if not self.accept(toktype, values):
            raise ValueError
        return


    def factor(self):
        if self.accept(TokenType.ID):
            return Variable(self.tok.value)

        elif self.accept(TokenType.NUMBER):
            return Number(self.tok.value)

        elif self.accept(TokenType.DELIMITER, ('(')):
            expr = self.expression()
            self.expect(TokenType.DELIMITER, (')'))
            return expr


    def term(self):
        factors = []
        n = self.factor()
        factors.append(Factor(None, n))
        while self.accept(TokenType.OPERATOR, ('*', '/')):
            op = self.tok.value
            n = self.factor()
            factors.append(Factor(op, n))

        return factors


    def expression(self):
        terms = []
        n = self.term()
        terms.append(Term(None, n))
        while self.accept(TokenType.OPERATOR, ('+', '-')):
            op = self.tok.value
            n = self.term()
            terms.append(Term(op, n))

        return Expression(terms)


    def assignment_statement(self):
        self.expect(TokenType.ID)
        var = Variable(self.tok.value)

        self.expect(TokenType.DELIMITER, ('='))
        expr = self.expression()
        return AssignmentStatement(var, expr)


    def condition(self):
        expr1 = self.expression()
        self.expect(TokenType.OPERATOR, ('==', '!=', '<', '<=', '>', '>='))
        op = self.tok.value
        expr2 = self.expression()
        return Condition(expr1, op, expr2)


    def if_statement(self):
        return


    def statement(self):
        if self.tokens_left() > 2 and self.tokens[1].type == TokenType.DELIMITER and self.tokens[1].value == '=':
            return self.assignment_statement()
        if self.accept(TokenType.KEYWORD, 'if'):
            return self.if_statement()
        else:
            return self.expression()


    def block(self):
        stats = []
        while not self.accept(TokenType.EOF):
            stat = self.statement()
            stats.append(stat)
        return Block(stats)


    def parse(self, tokens):
        self.tokens = tokens
        return self.block()
