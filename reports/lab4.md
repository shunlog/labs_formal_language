- [Lab 4: Chomsky normal form](#org9af32ec)
- [Theory](#org6bf9e9c)
- [Objectives](#org83cc369)
- [Results](#org71fc9fb)
- [Implementation](#orgb2788d2)




<a id="org9af32ec"></a>

# Lab 4: Chomsky normal form

Course
: Formal Languages &amp; Finite Automata

Author
: Balan Artiom


<a id="org6bf9e9c"></a>

# Theory


<a id="org83cc369"></a>

# Objectives

-   [X] Implement a method to convert a CFG to its normal form


<a id="org71fc9fb"></a>

# Results

```python
g1 = Grammar(VN = {'S', 'A', 'B', 'C', 'E'},
        VT = {'d', 'a'},
        S = 'S',
        P = {
            ('S',): {('A',)},
            ('A',): {('d',), ('d', 'S'), ('a', 'A', 'd', 'A', 'B')},
            ('B',): {('a', 'C'), ('a', 'S'), ('A', 'C')},
            ('C',): {()},
            ('E',): {('A', 'S')}})

"$$\n" + g1.to_latex() + '\n$$'
```

\\[
S → A
A → d S | d | a A d A B
B → A C | a S | a C
C → ε
E → A S
\\]


<a id="orgb2788d2"></a>

# Implementation

