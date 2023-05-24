- [Lab 5: Parsing, building an Abstract Syntax Tree](#orgb3fc8d3)
- [Theory](#org30f7605)
- [Objectives](#org455daa8)
- [Results](#org2d2b284)
- [Implementation](#orgc2b44f5)
- [Conclusion](#org3e459bb)




<a id="orgb3fc8d3"></a>

# Lab 5: Parsing, building an Abstract Syntax Tree

Course
: Formal Languages &amp; Finite Automata

Author
: Balan Artiom


<a id="org30f7605"></a>

# Theory

There are a dozen different parsers with different workings and different capabilities.
The easiest to implement seems to be the so-called [Recursive descent parser](https://en.wikipedia.org/wiki/Recursive_descent_parser).
To put it shortly, it is implemented by writing a function for every non-terminal in the grammar
which picks a suitable production from that non-terminal, consumes the tokens
and calls some other such functions when it meets other non-terminals,
then returns a part of the AST corresponding to its non-terminal.
Once we have such functions for every non-terminal,
we simply call the function for the starting symbol (e.g. `program`)
and watch in awe the magic of recursion do its thing.

An [abstract syntax tree](https://en.wikipedia.org/wiki/Abstract_syntax_tree) (AST) is an abstract representation of the syntax of a parsed text (duh?).
It differs from a parse tree in that it&rsquo;s not every token needs to corresponds to a node in the tree.
The image from the wikipedia page is very explanatory.


<a id="org455daa8"></a>

# Objectives

-   [X] Use a TokenType enum
-   [X] Use regex in the lexer
-   [X] Implement a parser that returns an AST


<a id="org2d2b284"></a>

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

# expressions can have parantheses
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


<a id="orgc2b44f5"></a>

# Implementation

First of all, the parser is written for a subset of Python.
Here&rsquo;s the grammar that I used as a guide:

```text
block = statement+
statement = expression
          | assignment_statement
          | conditional_statement
          | while_statement
assignment_statement = ID '=' expression
conditional_statement = 'if' condition ':' INDENT block DEDENT
      ('else' ':' INDENT block DEDENT)?
condition = expression ("==" | "!=" | ">" | "<" | ">=" | "<=") expression
while_statement = 'while' condition ':' INDENT block DEDENT
expression = term (("+"|"-") term)*
term = factor (("*"|"/") factor)*
factor = ID | Number | "(" expression ")"
```

The data structure I&rsquo;ve used for the AST representation is classes (duh).
Here&rsquo;s a few examples:

```python
...

@dataclass
class ConditionalStatement:
    condition: Condition
    then_block: Block
    else_block: Block

@dataclass
class Block:
    statements: list[Union[Expression, AssignmentStatement]]

...

@dataclass
class Number:
    value: str

...
```

The `@dataclass` line is a class decorator which automatically generates the constructors based on the member variables, effectively rendering the classes as `record`&rsquo;s in Pascal (or `struct`&rsquo;s in C).

I&rsquo;ve used the AST just for structuring, meaning I haven&rsquo;t implemented any evaluation capabilities

The `Parser` class has a few useful methods that I&rsquo;ve implemented
so I don&rsquo;t use its `tokens` list directly, because what if I want to change its representation later?.
Plus, this helped me implement the parser from the conceptual description of it found on Wikipedia.

```python
class Parser:
    # self.tok holds the previously consumed token
    # self.token holds the list of tokens,

    def next_tok(self):
        '''Returns the next token without consuming it.'''
        return self.tokens[0]


    def consume_tok(self):
        '''Consumes the next token and returns it.'''
        return self.tokens.pop(0)


    def accept(self, toktype, values=()):
        '''
        If next token is toktype, consumes it and returns it,
        otherwise don't consume it and return False.
        '''
        if self.tokens_left() and self.next_tok().type == toktype \
            and (not values or self.next_tok().value in values):
            self.tok = self.consume_tok()
            return True
        return False


    def expect(self, toktype, values=()):
        '''
        If next token is not toktype, raise error, otherwise return the token.
        '''
        if not self.accept(toktype, values):
            raise ValueError
        return
```

The meat of the parser consists of the recursive procedures corresponding to each terminal.
Here&rsquo;s the root method, `parse()`,
which initializes the list of tokens and calls the `block()` procedure:

```python
def parse(self, tokens):
    self.tokens = tokens
    return self.block()
```

Let&rsquo;s look at the  `statement()` procedure:

```python
def statement(self):
    if self.tokens_left() > 2 and self.tokens[1].type == TokenType.DELIMITER and self.tokens[1].value == '=':
        return self.assignment_statement()
    if self.accept(TokenType.KEYWORD, 'if'):
        return self.conditional_statement()
    if self.accept(TokenType.KEYWORD, 'while'):
        return self.while_statement()
    else:
        return self.expression()
```

It demonstrates the general working of these methods.
A `statement` has multiple production rules, but we can only pick one.
We do that by peeking at the next tokens (usually the first next)
and make a decision based on that.
Then, we look at the right hand side of the picked rule,
and for each non-terminal we call its procedure.
Simple as that!

Let&rsquo;s look at the `block()` procedure.

```python
def block(self):
    stats = []
    if self.accept(TokenType.INDENT):
        while not self.accept(TokenType.DEDENT):
            stat = self.statement()
            stats.append(stat)
    else:
        while not self.accept(TokenType.EOF):
            stat = self.statement()
            stats.append(stat)
    return Block(stats)
```

Notice in the grammar that a `block` is a list of statements,
so we initialize the list `stats`.
In this particular case, we need to check whether a `block` is delimited by `INDENT`&rsquo;s,
or if it ends with an `EOL`.
Once it&rsquo;s decided on that, it calls the `statement()` procedure.

Let&rsquo;s look at yet another scenario.

```python
def while_statement(self):
    # the 'while' has been consumed
    cond = self.condition()
    self.expect(TokenType.DELIMITER, ':')
    blck = self.block()
    return WhileStatement(cond, blck)
```

A `while` statement&rsquo;s first line ends with a terminal (the &rsquo;:&rsquo; character).
We don&rsquo;t need to write a procedure for it
since there&rsquo;s no information that could be parsed from a single character,
however we do expect it to be there.
That&rsquo;s what the `expect()` method is for - it errors out if the token is not there,
otherwise it consumes it.

That&rsquo;s pretty much it,
the rest of the code is pretty much one of the cases I&rsquo;ve shown above.


<a id="org3e459bb"></a>

# Conclusion

Implementing a simple parser by hand is not rocket science,
but I imagine that it wouldn&rsquo;t be feasible for more complicated languages.

However, it&rsquo;s pretty repetitive
which makes it rather difficult to test.
I had to manually write a test case for each production rule to ensure that it works correctly,
which is time-consuming and error-prone.
Parser generators like `ANTLR` are a better choice when writing an actual language, I think.

