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
    A -> aB
    A -> ε
    B -> b

    Is represented by the following variables

    VN = {"A", "B"}
    VT = {"a", "b"}
    P = {
        ("A"): [("a", "B"), ("a", "A"), ()],
        ("B"): [("b",)]
    }
    S = "A"
    '''
    def __init__(self, VN, VT, P, S):
        self.VN = VN
        self.VT = VT
        self.P = P
        self.S = S

    def type(self):

        def rule_type(head, tail):
            if len(head) == 1 and \
                (len(tail) == 0 or \
                len(tail) == 1 and tail[0] in self.VT or \
                len(tail) == 2 and tail[0] in self.VT and tail[1] in self.VN):
                return 3
            elif len(head) == 1:
                return 2
            else:
                for i,l in enumerate(head):
                    if l not in self.VN:
                        continue
                    a = head[:i]
                    b = head[i+1:]
                    ic(tail[-len(b):])
                    if a == tail[:i] and \
                       b == (tail[-len(b):] if len(b) != 0 else '') and \
                       len(head) <= len(tail):
                        return 1
                return 0

        return min([rule_type(h, t) for h in self.P.keys() for t in self.P[h]])

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


class NFA:
    '''
    A Finite State Machine is represented by 4 variables:
    S - set of states (strings)
    s0 - initial state (string)
    d - the state-transition function (dictionary: (state, rule) -> list of rules)
    F - set of final states (must be subset of S)

    Each rule in the regular grammar is treated as follows:
    1) A -> aB
        - a transition is created: (A, a): B
    2) A -> a
        - a transition is created: (A, a): ε
        - a final state is added: ε
    3) B -> ε,
        - a final state is added: B

    Example:

    The formal grammar

    A -> aA
    A -> aB
    A -> ε
    B -> b

    is transformed into the following NFA:
    S = {'B', 'ε', 'A'}
    s0 = 'A'
    d = {('A', 'a'): 'A', ('B', 'b'): 'ε'}
    F = {'ε', 'A'}
    '''
    def __init__(self, S, s0, d, F):
        self.S = S  # states
        self.s0 = s0  # initial state
        self.d = d  # transitions
        self.F = F # final states (subset of S)

    def from_grammar(g : Grammar):
        d = {}
        F = set()
        for head, tails in g.P.items():
            for tail in tails:
               if len(tail) == 0:
                   F |= {head}
               elif len(tail) == 1:
                   d |= {(head, tail[0]): "ε"}
                   F |= {"ε"}
               elif len(tail) == 2:
                   d |= {(head, tail[0]): tail[1]}
        return NFA(S = g.VN | F, s0 = g.S, d = d, F = F)

    def verify(self, w):
        s = self.s0
        for l in w:
            s2 = self.d.get((s, l))
            if not s2:
                return False
            s = s2
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
    # VN = {"S", "R", "L"}
    # VT = {"a", "b", "c", "d", "e", "f"}
    # P = {("S"): [( "a" , "S" ), ( "b", "S" ), ( "c", "R" ), ( "d", "L" )],
    #      ("R"): [( "d", "L" ), ( "e" )],
    #      ("L"): [( "f", "L" ), ( "e", "L" ), ( "d" )]}
    # S = "S"

    # Deterministic Regular grammar
    VN = {"A", "B"}
    VT = {"a", "b"}
    P = {("A"): [("a", "B"), ("a", "A"), ()],
        ("B"): [("b",)]}
    S = "A"

    g = Grammar(VN, VT, P, S)
    ic(g.type())

    # m, ml = "", 0
    # for _ in range(1000):
    #     w = g.constr_word()
    #     if len(w) > ml:
    #         ml = len(w)
    #         m = w
    # ic(m)
    # fsm = NFA.from_grammar(g)
    # ic(fsm)

    # for i in range(10):
    #     w = g.constr_word()
    #     ic(w)
    #     assert(fsm.verify(w))
    #     assert(not fsm.verify(w+"!"))
