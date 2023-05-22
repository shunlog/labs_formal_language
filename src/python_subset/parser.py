#!/usr/bin/env python3
from dataclasses import dataclass
from typing import Union
from icecream import ic

@dataclass
class Variable:
    name: str

@dataclass
class Number:
    value: str

@dataclass
class OpFactor:
    op: Union[str, None]
    factor: Union[Variable, Number, 'Expression']

@dataclass
class OpTerm:
    op: Union[str, None]
    term: list[OpFactor]

@dataclass
class Expression:
    opterms: list[OpTerm]


def expression(tokens):
    return None
