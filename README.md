# The title of the work

Course  
Formal Languages & Finite Automata

Author  
Balan Artiom

# Theory

An instance of a formal language is a set of *words* which are composed
of *letters*. The set of *words* can be defined in many ways:

- by simply enumerating all the valid elements (words)
- by defining an alphabet and a grammar
  alphabet  
  a set of *letters*

  grammar  
  a set of rules that define how to form valid *words* from the alphabet

# Objectives

Implement a `Grammar` and a `FiniteAutomaton`, with the respective
methods:

- `Grammar`
  - `generateString()`
  - `convert_to_FSM()`
- [ ] `FiniteAutomaton`
  - [ ] `check_string()`

Showcase the code:

- generate 5 words with the grammar
- create a FSM from the grammar
- check that the generated words are valid according to the FSM

# Implementation

To construct words with the grammar, I simply picked a random rule from
the list for each non-terminal and built the word until it hit a
terminal symbol.

``` python
def constr_word(self):
    from random import choice
    w = self.S
    while w[-1] in self.VN:
        # There's a slight probability this will go on for too long
        N = w[-1]
        w = w[:-1] + choice(self.P[N])
    return w
```

To convert the grammar to an FSM, I create a dictionary that maps each
pair `(state, letter)` to the next state `(new_state)`.

``` python
def to_FSM(self):
    fin_state = "End"
    d = {}
    for s0, arr in self.P.items():
        for v in arr:
            l = v[0]
            s1 = v[1] if len(v) == 2 else fin_state
            d[(s0, l)] = s1

    return FSM(self.VN | {fin_state}, self.S, d, {fin_state})
```

Verifying a word is done by going through each letter and doing the
transition from the current state according to the rule from the
dictionary of transitions. If there isn't such a transition, the word is
not valid. If in the end the current state is not a final state, the
word is not valid.

``` python
def verify(self, w):
    s = self.s0
    for l in w:
        ns = self.d.get((s, l))
        if not ns:
            return False
        s = ns
    return s in self.F
```

I made a few assumptions that would simplify the implementation:

- all symbols are strings of length 1
- there is only one terminal and at most one non-terminal symbol in a
  rule
- the non-terminal symbol comes after the terminal one
- the language defined by the grammar is deterministic

Variant \#3 defines a non-deterministic language, but not \#2 for
example. I'm not sure if this was intended, but to bring justice I
picked \#2 even though I'm 3rd on the list.
