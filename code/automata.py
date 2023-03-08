from grammar import Grammar
from collections import defaultdict

class NFA:
    '''
    This Nondeterministic finite automaton is represented by 4 variables:
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
    d = {('A', 'a'): {'A', 'B'}, ('B', 'b'): {'ε'}}
    F = {'ε', 'A'}
    '''
    def __init__(self, S, s0, d, F):
        self.S = S  # states
        self.s0 = s0  # initial state
        self.d = d  # transitions
        self.F = F # final states (subset of S)

    def from_grammar(g : Grammar):
        '''This function only recognizes *strictly* regular grammars'''
        d = defaultdict(set)
        F = set()
        for head, tails in g.P.items():
            for tail in tails:
               if len(tail) == 0:
                   F |= {head}
               elif len(tail) == 1:
                   d[(head, tail[0])] |= {"ε"}
                   F |= {"ε"}
               elif len(tail) == 2:
                   d[(head, tail[0])] |= {tail[1]}
        d = dict(d)
        return NFA(S = g.VN | F, s0 = g.S, d = d, F = F)

    def to_grammar(self) -> Grammar:
        VT = {k[1] for k in self.d.keys()}

        P = defaultdict(set)
        for k, v in self.d.items():
            P[k[0]] |= {(k[1], s) if s != "ε" else (k[1],) for s in v}
        for s in self.F:
            if s == "ε":
                continue
            P[s] |= {tuple()}
        P = dict(P)

        return Grammar(VN = self.S - {"ε"}, VT = VT, P = P, S = self.s0)

    def is_deterministic(self):
       return all([len(l) == 1 for l in self.d.values()])

    def __repr__(self):
        return ', '.join([str(x) for x in [self.S, self.s0, self.d, self.F]])


class DFA:
    '''
    This Deterministic finite automaton is similar to the NFA,
    with the distinction that states are now represented by sets, and not strings.
    For example, in the transitions dict,
    each destination state is a set denoting a single "node" in the DFA graph,
    not multiple possible states like in the case of an NFA.
    The other variables, S, s0 and F also reflect this change.

    Example:

    The NFA:
    S = {'B', 'ε', 'A'}
    s0 = 'A'
    d = {('A', 'a'): {'A', 'B'}, ('B', 'b'): {'ε'}}
    F = {'ε', 'A'}

    is transformed into the following DFA:
    S = {{'A'}, {'A', 'B'}, {'ε'}}
    s0 = {'A'}
    d = {
        ({'A'}, 'a'): {'A', 'B'},
        ({'A', 'B'}, 'a'): {'A', 'B'},
        ({'A', 'B'}, 'b'): {'ε'}
    }
    F = {{'A'}, {'A', 'B'}, {'ε'}}
    '''
    def __init__(self):
        pass

    def from_NFA():
        pass

    def verify(self, w):
        s = self.s0
        for l in w:
            s2 = self.d.get((s, l))
            if not s2:
                return False
            s = s2
        return s in self.F
