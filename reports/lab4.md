
# Table of Contents

1.  [Lab 4: Chomsky normal form](#org3670dea)
2.  [Theory](#orge3546e5)
3.  [Objectives](#orge595e4e)
4.  [Results](#orgc4a29be)
5.  [Implementation](#org3647dc7)



<a id="org3670dea"></a>

# Lab 4: Chomsky normal form

-   **Course:** Formal Languages & Finite Automata
-   **Author:** Balan Artiom


<a id="orge3546e5"></a>

# Theory


<a id="orge595e4e"></a>

# Objectives

-   [X] Implement a method to convert a CFG to its normal form


<a id="orgc4a29be"></a>

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
S → A
A → d S | d | a A d A B
B → A C | a S | a C
C → ε
E → A S
$$


<a id="org3647dc7"></a>

# Implementation

