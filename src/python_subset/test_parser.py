#!/usr/bin/env python3

import pytest
from parser import *
from lexer import *

@pytest.mark.parametrize("tokens, AST",[
    # '1'
    (
        [Token(TokenType.NUMBER, '1')],
        Expression([Term(None, [Factor(None, Number('1'))])])
    ),

    # 'a + 1'
    (
        [
            Token(TokenType.ID, 'a'),
            Token(TokenType.OPERATOR, '+'),
            Token(TokenType.NUMBER, '1')
        ],

        Expression(
            [Term(
                None,
                [Factor(
                    None,
                    Variable('a')
                )]
            ),
             Term(
                 '+',
                 [Factor(
                     None,
                     Number('1')
                 )]
             )]
        )
    ),


    # '10 * ab'
    (
        [
            Token(TokenType.NUMBER, '10'),
            Token(TokenType.OPERATOR, '*'),
            Token(TokenType.ID, 'ab')
        ],

        Expression(
            [Term(None,
                  [
                      Factor(None, Number('10')),
                      Factor('*', Variable('ab'))
                  ]
                  )]
        )
    ),

    # 'a1 + 10 - a2'
    (
        [
            Token(TokenType.ID, 'a1'),
            Token(TokenType.OPERATOR, '+'),
            Token(TokenType.NUMBER, '10'),
            Token(TokenType.OPERATOR, '-'),
            Token(TokenType.ID, 'a2')
        ],

        Expression(
            [
                Term(None, [Factor(None, Variable('a1'))]),
                Term('+', [Factor(None, Number('10'))]),
                Term('-', [Factor(None, Variable('a2'))]),
            ]
        )
    ),

    # '(a + b) * c'
    (
        [
            Token(TokenType.DELIMITER, '('),
            Token(TokenType.ID, 'a'),
            Token(TokenType.OPERATOR, '+'),
            Token(TokenType.ID, 'b'),
            Token(TokenType.DELIMITER, ')'),
            Token(TokenType.OPERATOR, '*'),
            Token(TokenType.ID, 'c')
        ],

        Expression([
            Term(None, [
                Factor(None, Expression([
                    Term(None, [Factor(None, Variable('a'))]),
                    Term('+', [Factor(None, Variable('b'))])
                ])),
                Factor('*', Variable('c')),
            ])])
    ),


    # 'a = 1'
    (
        [
            Token(TokenType.ID, 'a'),
            Token(TokenType.DELIMITER, '='),
            Token(TokenType.NUMBER, '1')
        ],
        AssignmentStatement(
            Variable('a'),
            Expression([Term(None, [Factor(None, Number('1'))])])
        )
    ),
])
def test_expr(tokens, AST):
    p = Parser()
    assert p.parse(tokens) == AST
