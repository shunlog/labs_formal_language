- [Lab 5: Parsing, building an Abstract Syntax Tree](#org02a5fc8)
- [Theory](#org643b7b5)
- [Objectives](#org39a29cc)
- [Results](#org3dc9054)
- [Implementation](#org38946c3)




<a id="org02a5fc8"></a>

# Lab 5: Parsing, building an Abstract Syntax Tree

Course
: Formal Languages &amp; Finite Automata

Author
: Balan Artiom


<a id="org643b7b5"></a>

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


<a id="org39a29cc"></a>

# Objectives

-   [X] Use a TokenType enum
-   [X] Use regex in the lexer
-   [X] Implement a parser that returns an AST


<a id="org3dc9054"></a>

# Results

```text
a + 10
```

```python
tokens = get_tokens(inp)

p = Parser()
ast = p.parse(tokens)
pprint(ast)
```

```text
Block(statements=[Expression(terms=[Term(op=None,
                                         factors=[Factor(op=None,
                                                         value=Variable(name='a'))]),
                                    Term(op='+',
                                         factors=[Factor(op=None,
                                                         value=Number(value=10))])])])
```


<a id="org38946c3"></a>

# Implementation

