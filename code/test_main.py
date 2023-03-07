#!/usr/bin/env python3
from main import *

def test_regular_grammar():
    '''
    A -> aA
    A -> aB
    A -> ε
    B -> b
    '''
    VN = {"A", "B"}
    VT = {"a", "b"}
    S = "A"
    P = {("A"): [("a", "B"), ("a", "A"), ()],
         ("B"): [("b",)]}
    g = Grammar(VN, VT, P, S)

    assert g.type() == 3

def test_context_sensitive_grammar():
    VN = {"A", "B"}
    VT = {"a", "b"}
    S = "A"
    P = {("abAbC"): [("abAbC")]}
    g = Grammar(VN, VT, P, S)
    assert g.type() == 1

    P = {("abbC"): [("abAbC")]}
    g = Grammar(VN, VT, P, S)
    assert g.type() != 1

    P = {("abAbC"): [("abbC")]}
    g = Grammar(VN, VT, P, S)
    assert g.type() != 1

    P = {("abAbC"): [("abxxxbC")]}
    g = Grammar(VN, VT, P, S)
    assert g.type() == 1

    P = {("AbC"): [("xxxbC")]}
    g = Grammar(VN, VT, P, S)
    assert g.type() == 1

    P = {("bCA"): [("bCB")]}
    g = Grammar(VN, VT, P, S)
    assert g.type() == 1
