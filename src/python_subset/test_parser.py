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
    )

])
def test_expr(tokens, AST):
    p = Parser()
    assert p.parse(tokens) == AST
