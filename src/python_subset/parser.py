#!/usr/bin/env python3
from dataclasses import dataclass
from typing import Union
from lexer import *
from icecream import ic

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


class Parser:
    def accept(self, toktype, values=()):
        # if first token is toktype, consume it and return it
        # otherwise don't consume it and return False
        if self.tokens and self.tokens[0].type == toktype \
            and (not values or self.tokens[0].value in values):
            self.tok = self.tokens.pop(0)
            return True
        return False


    def expect(self, toktype, values=()):
        # if next token is not toktype, raise error,
        # otherwise return the token
        if not self.accept(toktype, values):
            raise ValueError
        return



    def factor(self):
        if self.accept(TokenType.ID):
            return Variable(self.tok.value)
        elif self.accept(TokenType.NUMBER):
            return Number(self.tok.value)


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


    def parse(self, tokens):
        self.tokens = tokens
        return self.expression()
