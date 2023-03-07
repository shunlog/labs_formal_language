#!/usr/bin/env python3
from icecream import ic

class Grammar:
    '''
    A grammar is represented by 4 variables:
    VN - list of nonterminals (strings)
    VT - list of terminals (strings)
    P - list of productions represented by a dictionary, where
        keys are rules and values are lists of rules.
        A rule is a tuple of terminals and nonterminals

    Example:

    The formal grammar

    A -> aA
    A -> bB
    A -> B
    B -> ε

    Is represented by the following variables

    VN = {"A", "B"}
    VT = {"a", "b"}
    P = {
        ("A"): [("a", "A"), ("b", "B"), ("B")],
        ("B"): [()]
    }
    S = "A"
    '''
    def __init__(self, VN, VT, P, S):
        self.VN = VN
        self.VT = VT
        self.P = P
        self.S = S

    def constr_word(self):
        '''Assuming *strictly* right-regular grammar,
        build a word by randomly picking rules to rewrite'''
        from random import choice
        s = self.S  # current state
        w = ""  # word
        while True:
            tail = choice(self.P[(s)])
            if len(tail) == 2:
                w += tail[0]
                s = tail[1]
            elif len(tail) == 1:
                w += tail[0]
                break
            elif len(tail) == 0:
                break
        return ''.join(w)


class FSM:
    '''
    A Finite State Machine is represented by 4 variables:
    S - set of states (strings)
    s0 - initial state (string)
    d - the state-transition function (dictionary: (state, rule) -> list of rules)
    F - set of final states (must be subset of S)
    '''
    def __init__(self, S, s0, d, F):
        self.S = S  # states
        self.s0 = s0  # initial state
        self.d = d  # transitions
        self.F = F # final states (subset of S)

    def from_grammar(g : Grammar):
        d = {}
        for head, tail in g.P.items():
            d |= {(head, v[0]): v[1] if len(v) > 1 else "ε" for v in tail}
        return FSM(S = g.VN | {"ε"},
                   s0 = g.S,
                   d = d,
                   F = {"ε"})

    def verify(self, w):
        s = self.s0
        for l in w:
            ns = self.d.get((s, l))
            if not ns:
                return False
            s = ns
        return s in self.F

    def __repr__(self):
        return ', '.join([str(x) for x in [self.S, self.s0, self.d, self.F]])

if __name__ == '__main__':
    # Variant #3 is non-deterministic (didn't reserve enough time for that)
    # VN=["S", "D", "R"]
    # VT=["a", "b", "c", "d", "f"]
    # P={"S": ["aS", "bD", "fR"],
    #     "D": ["cD", "dR", "d"],
    #     "R": ["bR", "f"]}
    # S = "S"

    # Variant #2
    VN = {"S", "R", "L"}
    VT = {"a", "b", "c", "d", "e", "f"}
    P = {("S"): [( "a" , "S" ), ( "b", "S" ), ( "c", "R" ), ( "d", "L" )],
         ("R"): [( "d", "L" ), ( "e" )],
         ("L"): [( "f", "L" ), ( "e", "L" ), ( "d" )]}
    S = "S"

    g = Grammar(VN, VT, P, S)
    m, ml = "", 0
    for _ in range(1000):
        w = g.constr_word()
        if len(w) > ml:
            ml = len(w)
            m = w
    ic(m)
    fsm = FSM.from_grammar(g)
    ic(fsm)

    # for i in range(10):
    #     w = g.constr_word()
    #     assert(fsm.verify(w))
    #     assert(not fsm.verify(w+"a"))
