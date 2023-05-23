- [Lab 5: Parsing, building an Abstract Syntax Tree](#org7816020)
- [Theory](#orge54962b)
- [Objectives](#org3793804)
- [Results](#org5e6069a)
- [Implementation](#org3f4c15f)




<a id="org7816020"></a>

# Lab 5: Parsing, building an Abstract Syntax Tree

Course
: Formal Languages &amp; Finite Automata

Author
: Balan Artiom


<a id="orge54962b"></a>

# Theory

There are a dozen different parsers with different workings and different capabilities.
The easiest to implement seems to be the so-called [Recursive descent parser](https://en.wikipedia.org/wiki/Recursive_descent_parser).
To put it shortly, it is implemented by writing a function for every non-terminal in the grammar
which picks a suitable production from that non-terminal, consumes the tokens
and calls some other such functions when it meets other non-terminals,
then returns a part of the AST corresponding to its non-terminal.
Once we have such functions for every non-terminal,
we simply call the function for the starting symbol (e.g. `program`)
and watch in awe the magic of recursion do its thing..


<a id="org3793804"></a>

# Objectives

-   [X] Use a TokenType enum
-   [X] Use regex in the lexer
-   [X] Implement a parser that returns an AST


<a id="org5e6069a"></a>

# Results


<a id="org3f4c15f"></a>

# Implementation

