- [Lab 5: Parsing, building an Abstract Syntax Tree](#org55c6ba8)
- [Theory](#org435ea81)
- [Objectives](#orge4e228c)
- [Results](#orga299b6a)
- [Implementation](#orge304492)




<a id="org55c6ba8"></a>

# Lab 5: Parsing, building an Abstract Syntax Tree

Course
: Formal Languages &amp; Finite Automata

Author
: Balan Artiom


<a id="org435ea81"></a>

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


<a id="orge4e228c"></a>

# Objectives

-   [X] Use a TokenType enum
-   [X] Use regex in the lexer
-   [X] Implement a parser that returns an AST


<a id="orga299b6a"></a>

# Results

The result of my hard work is this parser for a subset of Python (kind of):

```python
p = Parser()
```

Without further ado, let me show it in action. Here&rsquo;s a little program which consists of a single expression:

```python
a + 10
```

And here&rsquo;s how I can parse it:

```python
tokens = get_tokens(inp)
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

Great, isn&rsquo;t it? Of course it would&rsquo;ve been better if I could draw it,
but `pprint()` is good enough, you can still see the tree structure.

Let&rsquo;s see some more examples. Here&rsquo;s a list of assignments with comments:

```python
# comments and blank lines are ignored

# assignments can have parantheses
a = 10 * (5 + 5 * 2)
b = 1 * 2 / 3 * 4
```

And here&rsquo;s the AST:

```python
tokens = get_tokens(inp)
ast = p.parse(tokens)

pprint(ast)
```

```text
Block(statements=[AssignmentStatement(var=Variable(name='a'),
                                      expr=Expression(terms=[Term(op=None,
                                                                  factors=[Factor(op=None,
                                                                                  value=Number(value=10)),
                                                                           Factor(op='*',
                                                                                  value=Expression(terms=[Term(op=None,
                                                                                                               factors=[Factor(op=None,
                                                                                                                               value=Number(value=5))]),
                                                                                                          Term(op='+',
                                                                                                               factors=[Factor(op=None,
                                                                                                                               value=Number(value=5)),
                                                                                                                        Factor(op='*',
                                                                                                                               value=Number(value=2))])]))])])),
                  AssignmentStatement(var=Variable(name='b'),
                                      expr=Expression(terms=[Term(op=None,
                                                                  factors=[Factor(op=None,
                                                                                  value=Number(value=1)),
                                                                           Factor(op='*',
                                                                                  value=Number(value=2)),
                                                                           Factor(op='/',
                                                                                  value=Number(value=3)),
                                                                           Factor(op='*',
                                                                                  value=Number(value=4))])]))])
```

Notice how the AST consists of a `Block`, which has two `AssignmentStatement`,
which have two fields, `var` and `expr`.
The `Expression` structure is a bit fancy to allow for operator precedence.
Here&rsquo;s the relevant piece of grammar to explain it:

```text
expression = term (("+"|"-") term)*
term = factor (("*"|"/") factor)*
factor = ID | Number | "(" expression ")"
```

The last things I haven&rsquo;t showcased yet are conditionals and `while` statements:

```python
while b == 0:
    if a > b:
        a = a - b
    else:
        b = b - a
```

```python
tokens = get_tokens(inp)
ast = p.parse(tokens)

pprint(ast)
```

```text
Block(statements=[WhileStatement(condition=Condition(expr1=Expression(terms=[Term(op=None,
                                                                                  factors=[Factor(op=None,
                                                                                                  value=Variable(name='b'))])]),
                                                     op='==',
                                                     expr2=Expression(terms=[Term(op=None,
                                                                                  factors=[Factor(op=None,
                                                                                                  value=Number(value=0))])])),
                                 block=Block(statements=[ConditionalStatement(condition=Condition(expr1=Expression(terms=[Term(op=None,
                                                                                                                               factors=[Factor(op=None,
                                                                                                                                               value=Variable(name='a'))])]),
                                                                                                  op='>',
                                                                                                  expr2=Expression(terms=[Term(op=None,
                                                                                                                               factors=[Factor(op=None,
                                                                                                                                               value=Variable(name='b'))])])),
                                                                              then_block=Block(statements=[AssignmentStatement(var=Variable(name='a'),
                                                                                                                               expr=Expression(terms=[Term(op=None,
                                                                                                                                                           factors=[Factor(op=None,
                                                                                                                                                                           value=Variable(name='a'))]),
                                                                                                                                                      Term(op='-',
                                                                                                                                                           factors=[Factor(op=None,
                                                                                                                                                                           value=Variable(name='b'))])]))]),
                                                                              else_block=Block(statements=[AssignmentStatement(var=Variable(name='b'),
                                                                                                                               expr=Expression(terms=[Term(op=None,
                                                                                                                                                           factors=[Factor(op=None,
                                                                                                                                                                           value=Variable(name='b'))]),
                                                                                                                                                      Term(op='-',
                                                                                                                                                           factors=[Factor(op=None,
                                                                                                                                                                           value=Variable(name='a'))])]))]))]))])
```


<a id="orge304492"></a>

# Implementation

