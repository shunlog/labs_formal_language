- [Implementation of formal languages](#orgf8191f4)
- [Theory](#orgd5f3527)
- [Objectives](#orgce8c013)
- [Results](#org7709b3f)
    - [Convert NFA to Grammar](#org8a42a60)
    - [Find out if FA is nondeterministic](#org4fe69a3)
    - [Convert NFA to DFA](#org6b93b56)
    - [Visualize the finite automata](#org4a4f11e)
    - [Convert Grammar to NFA to DFA (lab 1)](#orgbaea10e)
- [Implementation](#org298a493)




<a id="orgf8191f4"></a>

# Implementation of formal languages

Course
: Formal Languages &amp; Finite Automata

Author
: Balan Artiom


<a id="orgd5f3527"></a>

# Theory

An instance of a **formal language** is a set of _words_ which are composed of _letters_.
The set of words can be defined in many ways:

-   by simply enumerating all the valid elements (words)
-   by defining an alphabet and a grammar

An **alphabet** is a set of letters.

A **grammar** is a set of rules that define how to form valid words from the alphabet.

A regular grammar is one in which all production rules in P are of one of the following forms:

-   A → a
-   A → aB
-   A → ε

where A, B, S ∈ N are non-terminal symbols, a ∈ Σ is a terminal symbol,
and ε denotes the empty string, i.e. the string of length 0. S is called the start symbol.

[Automata](https://en.wikipedia.org/wiki/Automata_theory) can be used to recognize formal languages, for example described by grammars.
There are different [types of automata](https://en.wikipedia.org/wiki/Automata_theory#Types_of_automata) that can describe different types of languages.
For example:

-   A finite automaton (NFA/DFA, state machine) can describe a regular grammar (type 3)
-   A pushdown automaton (PDA) can describe a context-free grammar (type 2)

A DFA is equivalent in power to an NFA, even though NFA&rsquo;s are more flexible ([Hierarchy in terms of powers](https://en.wikipedia.org/wiki/Automata_theory#Hierarchy_in_terms_of_powers)).

-   The conversion NFA -&gt; DFA can be done using the [powerset construction](https://en.wikipedia.org/wiki/Powerset_construction).
-   The conversion regular grammar -&gt; NFA and viceversa is straightforward.
-   The conversion Grammar -&gt; DFA can&rsquo;t really be done directly,
    instead go through the steps: Grammar -&gt; NFA -&gt; DFA.


<a id="orgce8c013"></a>

# Objectives

-   [X] Provide a function in your grammar type/class that could classify the grammar based on Chomsky hierarchy.
-   [X] Implement conversion of a finite automaton to a regular grammar.
-   [X] Determine whether your FA is deterministic or non-deterministic.
-   [X] Implement some functionality that would convert an NDFA to a DFA.
-   [X] Represent the finite automaton graphically (Optional, and can be considered as a bonus point):
-   [X] Document everything in the README
-   [X] Test string validation with the new more general DFA


<a id="org7709b3f"></a>

# Results

Here&rsquo;s the NFA I got:

```text
Q = {q0,q1,q2,q3,q4},
∑ = {a,b},
F = {q4},
δ(q0,a) = q1,
δ(q1,b) = q1,
δ(q1,a) = q2,
δ(q2,b) = q2,
δ(q2,b) = q3,
δ(q3,b) = q4,
δ(q3,a) = q1.
```

After manually rewriting it like this:

```python
S = {"q0","q1","q2","q3","q4"}
A = {"a","b"}
s0 = "q0"
F = {"q4"}
d = {("q0","a"): {"q1"},
     ("q1","b"): {"q1"},
     ("q1","a"): {"q2"},
     ("q2","b"): {"q2", "q3"},
     ("q3","b"): {"q4"},
     ("q3","a"): {"q1"}}
```

I can initialize an NFA, and then do many things with it.

```python
nfa = NFA(S=S, A=A, s0=s0, d=d, F=F)
```


<a id="org8a42a60"></a>

### Convert NFA to Grammar

I can find out the type of the resulting grammar in the Chomsky hierarchy:

```python
g = nfa.to_grammar()
print(g.type())
```

```text
3
```

Or print out the grammar if I format it a bit:

```python
for l,r in g.P.items():
    print(''.join(l), '->', ' | '.join([' '.join(t) for t in r]))
```

```text
q0 -> a q1
q1 -> b q1 | a q2
q2 -> b q2 | b q3
q3 -> b q4 | a q1
q4 ->
```


<a id="org4fe69a3"></a>

### Find out if FA is nondeterministic

Even though it&rsquo;s an NFA, it could be that it doesn&rsquo;t have nondeterministic transitions.
We can find that out:

```python
print(nfa.is_deterministic())
```

```text
False
```


<a id="org6b93b56"></a>

### Convert NFA to DFA

```python
dfa = nfa.to_DFA()
print(dfa)
```

```text
{frozenset({'q4', 'q2', 'q3'}), frozenset({'q2'}), frozenset({'q1'}), frozenset({'q0'}), frozenset({'q2', 'q3'})}, {'a', 'b'}, {'q0'}, {(frozenset({'q0'}), 'a'): {'q1'}, (frozenset({'q1'}), 'a'): {'q2'}, (frozenset({'q1'}), 'b'): {'q1'}, (frozenset({'q2'}), 'b'): {'q2', 'q3'}, (frozenset({'q2', 'q3'}), 'a'): {'q1'}, (frozenset({'q2', 'q3'}), 'b'): {'q4', 'q2', 'q3'}, (frozenset({'q4', 'q2', 'q3'}), 'a'): {'q1'}, (frozenset({'q4', 'q2', 'q3'}), 'b'): {'q4', 'q2', 'q3'}}, {frozenset({'q4', 'q2', 'q3'})}
```

Now that we have a DFA, we can easily validate some strings according to the grammar.
But first, let&rsquo;s generate a few:

```python
l = [g.constr_word() for _ in range(5)]
print(l)
```

```text
['aabbb', 'ababbababbbababb', 'abbbabbb', 'ababbb', 'aabbbb']
```

Let&rsquo;s verify that they&rsquo;re all valid:

```python
print(all(dfa.verify(w) for w in l))
```

```text
True
```


<a id="org4a4f11e"></a>

### Visualize the finite automata

Here&rsquo;s the NFA:

```python
fn = nfa.draw('./img', 'variant_3_nfa')
print(fn)
```

![img](img/variant_3_nfa.gv.svg)

And the DFA:

```python
fn = dfa.draw('./img', 'variant_3_dfa')
print(fn)
```

![img](img/variant_3_dfa.gv.svg)


<a id="orgbaea10e"></a>

### Convert Grammar to NFA to DFA (lab 1)

Extending on the previous lab task,
I can now do some things with the grammar I got:

```text
VN={S, D, R},
VT={a, b, c, d, f},
P={
    S → aS
    S → bD
    S → fR
    D → cD
    D → dR
    R → bR
    R → f
    D → d
}
```

After converting it manually to a Grammar data structure, of course:

```python
VN = {"S", "D", "R"}
VT = {"a", "b", "c", "d", "f"}
S = "S"
P = {("S",): {("a", "S"), ("b", "D"), ("f", "R")},
     ("D",): {("c", "D"), ("d", "R"), ("d")},
     ("R",): {("b", "R"), ("f")}}
g = Grammar(VN=VN, VT=VT, P=P, S=S)
```

Note that the keys in the `P` dict are tuples. Remember kids, `(A)` is not a tuple, but `(A,)` is.

Now, let&rsquo;s convert the grammar to an NFA:

```python
nfa = NFA.from_grammar(g)
print(nfa.draw('img', 'lab1_v3_nfa'))
```

![img](img/lab1_v3_nfa.gv.svg)

Hmm, looks like it&rsquo;s not deterministic because of those two &ldquo;d&rdquo; transitions from the &ldquo;D&rdquo; state. Let&rsquo;s check:

```python
print(nfa.is_deterministic())
```

```text
False
```

Yeah, it isn&rsquo;t. OK, no problem. We can just convert it to a DFA:

```python
dfa = nfa.to_DFA()
print(dfa.draw('img', 'lab1_v3_dfa'))
```

![img](img/lab1_v3_dfa.gv.svg)

Looks better!


<a id="org298a493"></a>

# Implementation

I wrote very extensive comments inside source code files, so refer to those please.

### API

This part of the documentation covers all the interfaces of **angryowl**.

#### Grammar


##### _class_ angryowl.grammar.Grammar(VN: set[str], VT: set[str], P: dict[tuple[str], set[tuple[str]]], S: str)

A grammar is represented by 4 variables:


;* **Parameters**


    * **VN** – list of nonterminals (strings)


    * **VT** – list of terminals (strings)


    * **P** – list of productions represented by a dictionary, where
    keys are rules and values are sets of rules.
    A rule is a tuple of terminals and nonterminals.
    Although, a rule can also be represented by a string
    if every symbol is a single character in length.


    * **S** – starting state (string)


For example, the formal grammar:

```default
A -> aA
A -> aB
A -> ε
B -> b
```

Is represented by the following variables:

```default
VN = {"A", "B"}
VT = {"a", "b"}
P = {
    ("A",): {("a", "B"), ("a", "A"), ()},
    ("B",): {("b",)}
}
S = "A"
```


###### Rule()

alias of `tuple`[`str`]


###### constr_word()

Assuming *strictly* right-regular grammar.


;* **Returns**

    A string built using rules from the grammar picked at random.


#### Automata


##### _class_ angryowl.automata.FA(S: set[str], A: set[str], s0: str, d: dict[tuple[set[str], str], set[str]], F: set[str])

A finite automaton is represented by 5 variables.


;* **Parameters**


    * **S** – set of states (set of strings)


    * **A** – alphabet, which is a set of symbols (set of strings)


    * **s0** – starting state (a string)


    * **d** – the state-transition function (dictionary: tuple(state, symbol) -> set of states)


    * **F** – set of final states (must be subset of S)



##### _class_ angryowl.automata.NFA(S: set[str], A: set[str], s0: str, d: dict[tuple[set[str], str], set[str]], F: set[str])

Each rule in the regular grammar is treated as follows:


1. A -> aB

>
>     * a transition is created: (A, a): B


>     * “a” is added to the alphabet


2. A -> a

>
>     * a transition is created: (A, a): ε


>     * a final state is added: ε


>     * “a” is added to the alphabet


3. B -> ε

>
>     * a final state is added: B

For example, the formal grammar:

```default
A -> aA
A -> aB
A -> ε
B -> b
```

is transformed into the following NFA:

```default
S = {'B', 'ε', 'A'}
A = {'a', 'b'}
s0 = 'A'
d = {('A', 'a'): {'A', 'B'}, ('B', 'b'): {'ε'}}
F = {'ε', 'A'}
```


###### from_grammar()

This function only recognizes *strictly* regular grammars


###### to_DFA()

For an explanation of the algo, check out the dragon book.


##### _class_ angryowl.automata.DFA(S: set[str], A: set[str], s0: str, d: dict[tuple[set[str], str], set[str]], F: set[str])

This Deterministic finite automaton is similar to the NFA,
with the distinction that states are now represented by sets, and not strings.
For example, in the transitions dict,
a value is a set of states denoting a single “node” in the DFA graph,
not multiple possible states like in the case of an NFA,
whereas the keys are now represented by tuple[set[State], Symbol]
The other variables, S, s0 and F also reflect this change.

For example, the NFA:

```default
S = {'B', 'ε', 'A'}
A = {'a', 'b'}
s0 = 'A'
d = {('A', 'a'): {'A', 'B'}, ('B', 'b'): {'ε'}}
F = {'ε', 'A'}
```

is transformed into the following DFA:

```default
S = {{'A'}, {'A', 'B'}, {'ε'}}
A = {'a', 'b'}
s0 = {'A'}
d = {
    ({'A'}, 'a'): {'A', 'B'},
    ({'A', 'B'}, 'a'): {'A', 'B'},
    ({'A', 'B'}, 'b'): {'ε'}
}
F = {{'A'}, {'A', 'B'}, {'ε'}}
```

