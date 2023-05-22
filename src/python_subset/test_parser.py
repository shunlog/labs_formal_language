#!/usr/bin/env python3

import pytest
from parser import *
from lexer import *

@pytest.mark.parametrize("tokens, AST",[

    # 'a + 1'
(
    [
        Token(TokenType.ID, 'a'),
        Token(TokenType.OPERATOR, '+'),
        Token(TokenType.NUMBER, '1')
    ],

    Expression(
        [OpTerm(
            None,
            [OpFactor(
                None,
                Variable('a')
            )]
        ),
         OpTerm(
             '+',
             [OpFactor(
                 None,
                 Number('1')
             )]
         )]
    )
)

])
def test_expr(tokens, AST):
    assert expression(tokens) == AST
