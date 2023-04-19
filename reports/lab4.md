
# Table of Contents

1.  [Lab 4: Chomsky normal form](#orga493fc5)
2.  [Theory](#org1799aba)
3.  [Objectives](#orga341e89)
4.  [Results](#orgc8b2a98)
5.  [Implementation](#orge7e9daa)



<a id="orga493fc5"></a>

# Lab 4: Chomsky normal form

-   **Course:** Formal Languages & Finite Automata
-   **Author:** Balan Artiom


<a id="org1799aba"></a>

# Theory


<a id="orga341e89"></a>

# Objectives

-   [X] Implement a method to convert a CFG to its normal form


<a id="orgc8b2a98"></a>

# Results

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

$$
S → A\\
A → d | a A d A B | d S\\
B → a S | a C | A C\\
C → ε\\
E → A S
$$


<a id="orge7e9daa"></a>

# Implementation

