# Mini Lisp Interpreter

A small Lisp-style interpreter written from scratch in Python.  

This project implements a minimal expression language capable of parsing, validating, and evaluating nested symbolic expressions such as:

```lisp
(ADD 2 (MUL 3 4))
```

The system builds an internal tree structure (AST-like), evaluates experessions recursively, and maintains a runtime variable memory similar to a simple programming language.  

The goal of this project is to demonstrate **software design**, **parsing logic**, **recursion**, and **interpreter architecture** rather than create a production language.  

## Features

### Expression Language

Supports prefix expressions with nested structure:

```lisp
(ADD (MUL 2 3) (DIV 8 4))
```

### Variable Assignment

Variables are stored in an internal memory table:

```lisp
(SET x 5)
(ADD x 3)
```

### Binary Operations

| **Operation**    |      **Description**                 |
| ---------------- | ------------------------------------ |
|       ADD        |      Addition                        |
| ---------------- | ------------------------------------ |
|       SUB        |      Subtraction                     |
| ---------------- | ------------------------------------ |
|       MUL        |      Multiplication                  |
| ---------------- | ------------------------------------ |
|       DIV        |      Division                        |
| ---------------- | ------------------------------------ |
|       LOG        |      Logarithm with custom base      |

#### Example

```lisp
(LOG 8 2)
```

### Unary Operations

| **Operation**    |      **Description**    |
| ---------------- | ----------------------- |
|       SQRT       |      Square root        |
| ---------------- | ----------------------- |
|       NEG        |      Negation           |
| ---------------- | ----------------------- |
|       ABS        |      Absolute value     |
| ---------------- | ----------------------- |
|       FACT       |      Factorial          |
| ---------------- | ----------------------- |
|       EXP        |      Exponential        |
| ---------------- | ----------------------- |
|       LOG2       |      Log base 2         |
| ---------------- | ----------------------- |
|       LOG10      |      Log base 10        |

#### Example

```lisp
(SQRT (ADD 9 7))
```

### Nested Expressions

Expressions can be nested arbitrarily deep:

```lisp
(ADD
    (MUL
        (ADD (SUB 10 5) (MUL 2 3))
        (DIV 20 (ADD 2 3))
    )
    (DIV
        (SUB (MUL 4 4) (ADD 3 1))
        (MUL 2 (SUB 5 3))
    )
)
```

### Program Execution Modes

#### Immediate execution
Evaluate one expression directly:

```Python
interp.Execute("(ADD 2 3)")
```

Output:
```Code
5
```

#### Stored program execution
Store multiple expressions and run them sequentially:

```Python
interp.Add("""
(SET x 5)
(SET y 4)
(ADD (MUL 5 x) (DIV y 2))
""")

interp.Run()
```

Output:
```Code
27
```

### Lisp-style Visualization

```Python
interp.Show(mode="lisp")
```

Output:
```Code
(PROGRAM)
    (SET x 5)
    (SET y 4)
    (ADD (MUL 5 x) (DIV y 2))
```

### Tree Visualization

Stored programs can be visualized as a tree:

```Python
interp.Show(mode="tree")
```

Output:
```Code
(PROGRAM)
│
├── SET x
│   └── 5
│
├── SET y
│   └── 4
│
└── ADD
    ├── DIV
    │   ├── y
    │   └── 2
    └── DIV
        ├── y
        └── 2
```

### Variable Memory Inspection

```Python
interp.Variable()
interp.Variable("x")
```

### Controlled Reset
Clear stored program.

```Python
interp.Clear()
```

Clear program and variables:

```Python
interp.Clear(variables=True)
```

### Error Handling

The interpreter validates syntax and runtime behavior.  

Examples of handled errors:  
- Incorrect number of arguments
- Undefined variables
- Invalid logarithm domains
- Division by zero
- Invalid variable names

Example:

```lisp
(ADD 1)
```
```Code
SyntaxError: Add expects 2 arguments, gor 1
```

## Project Structure

```Code
src/
    program.py
    node.py
    evaluator.py
    vartable.py

demo.ipynb
README.md
```

## Example Usage

```Python
from src.Program import Program

interp = Program()

interp.Add("""
(SET x 5)
(SET y (ADD x 10))
(SET x 20)
(MUL y x)
""")

interp.Show(mode="Tree")

interp.Run()

interp.Variable("x")
```

## Design Overview

The interpreter is built from several components:

- **Tokenizer**: Transforms input string into structured tokens.
- **Parser**: Buids a tree structure from nested expressions.
- **AST-like Node Structure**: Represents operations and values in hierarchical form.
- **Evaluator**: Recursively computes results from the tree.
- **Variable Table**: Stores runtime variable values.
- **Validator**: Ensures correct syntax and argument structure.

## Motivation

This project was developed to demonstrate:
- recursive parsing
- tree data structure
- interpreter design
- validation strategies
- separation of concerns
- API-style interface design

The entire system was implemented from scratch without relying on external parsing libraries.

## Future Improvements

Possible extensions:
- IF expression
- user-defined functions
- loops
- REPL interface
- packaging as installable module

## Demo Notebook

A complete interactive demonstration is available in:
```Code
demo.ipynb
```

The notebook includes examples of:
- basic operations
- nested expressions
- variable assignments
- tree visualization
- error handling
- program execution modes

## Requirements
- Python 3.10 or higher
- No external dependencies

## License
MIT License