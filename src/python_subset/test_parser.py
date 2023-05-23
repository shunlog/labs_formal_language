#!/usr/bin/env python3

import pytest
from parser import *
from lexer import *

@pytest.mark.parametrize("tokens, AST",[
    # '1'
    (
        [
            Token(TokenType.NUMBER, '1'),
            Token(TokenType.EOF)
        ],
        Block([Expression([Term(None, [Factor(None, Number('1'))])])])
    ),

    # 'a + 1'
    (
        [
            Token(TokenType.ID, 'a'),
            Token(TokenType.OPERATOR, '+'),
            Token(TokenType.NUMBER, '1'),
            Token(TokenType.EOF)
        ],

        Block([
            Expression([
                Term(None, [Factor(None, Variable('a'))]),
                Term('+', [Factor(None, Number('1'))])
            ])])
    ),


    # '10 * ab'
    (
        [
            Token(TokenType.NUMBER, '10'),
            Token(TokenType.OPERATOR, '*'),
            Token(TokenType.ID, 'ab'),
            Token(TokenType.EOF)
        ],

        Block([
            Expression([
                Term(None, [
                    Factor(None, Number('10')),
                    Factor('*', Variable('ab'))
                ])])
        ])
    ),

    # 'a1 + 10 - a2'
    (
        [
            Token(TokenType.ID, 'a1'),
            Token(TokenType.OPERATOR, '+'),
            Token(TokenType.NUMBER, '10'),
            Token(TokenType.OPERATOR, '-'),
            Token(TokenType.ID, 'a2'),
            Token(TokenType.EOF)
        ],

        Block([
            Expression([
                Term(None, [Factor(None, Variable('a1'))]),
                Term('+', [Factor(None, Number('10'))]),
                Term('-', [Factor(None, Variable('a2'))]),
            ])
        ])
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
            Token(TokenType.ID, 'c'),
            Token(TokenType.EOF)
        ],

        Block([
            Expression([
                Term(None, [
                    Factor(None, Expression([
                        Term(None, [Factor(None, Variable('a'))]),
                        Term('+', [Factor(None, Variable('b'))])
                    ])),
                    Factor('*', Variable('c')),
                ])
            ])
        ])
    ),


    # 'a = 1'
    (
        [
            Token(TokenType.ID, 'a'),
            Token(TokenType.DELIMITER, '='),
            Token(TokenType.NUMBER, '1'),
            Token(TokenType.EOF)
        ],
        Block([
            AssignmentStatement(
                Variable('a'),
                Expression([Term(None, [Factor(None, Number('1'))])])
            )])
    ),
])
def test_parse(tokens, AST):
    p = Parser()
    assert p.parse(tokens) == AST


@pytest.mark.parametrize("tokens, AST",[
    (
        # a == 1
        [
            Token(TokenType.ID, 'a'),
            Token(TokenType.OPERATOR, '=='),
            Token(TokenType.NUMBER, '1'),
        ],
        Condition(
            expr1 = Expression([Term(None, [Factor(None, Variable('a'))])]),
            op = '==',
            expr2 = Expression([Term(None, [Factor(None, Number('1'))])])
        )
    )

    ])
def test_condition(tokens, AST):
    p = Parser()
    # TODO: how do you test private methods without accessing private fields?
    p.tokens = tokens
    assert p.condition() == AST


@pytest.mark.parametrize("tokens, AST",[
    (
        # if a == 1:
        #     a = 2
        # else:
        #     a = 3
        [
            Token(TokenType.ID, 'a'),
            Token(TokenType.OPERATOR, '=='),
            Token(TokenType.NUMBER, '1'),
            Token(TokenType.DELIMITER, ':'),

            Token(TokenType.INDENT),
            Token(TokenType.ID, 'a'),
            Token(TokenType.DELIMITER, '='),
            Token(TokenType.NUMBER, '2'),
            Token(TokenType.DEDENT),

            Token(TokenType.KEYWORD, 'else'),
            Token(TokenType.DELIMITER, ':'),
            Token(TokenType.INDENT),
            Token(TokenType.ID, 'a'),
            Token(TokenType.DELIMITER, '='),
            Token(TokenType.NUMBER, '3'),
            Token(TokenType.DEDENT),
        ],

        ConditionalStatement(
            condition = Condition(
                expr1 = Expression([Term(None, [Factor(None, Variable('a'))])]),
                op = '==',
                expr2 = Expression([Term(None, [Factor(None, Number('1'))])]),
            ),
            then_block = Block([
                AssignmentStatement(
                    Variable('a'),
                    Expression([Term(None, [Factor(None, Number('2'))])])
                )
            ]),
            else_block = Block([
                AssignmentStatement(
                    Variable('a'),
                    Expression([Term(None, [Factor(None, Number('3'))])])
                )
            ])
        )
    )
])
def test_conditional_statement(tokens, AST):
    p = Parser()
    p.tokens = tokens
    assert p.conditional_statement() == AST
