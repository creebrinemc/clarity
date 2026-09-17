# Clarity 0.3.0 Specification

## Language philosophy

Clarity aims for readable, English-inspired syntax while keeping common code concise. Version 0.3.0 extends Clarity with user-defined functions, return values, lexical closures, first-class functions, and recursion.

## Lexical structure

Source is line-oriented. Spaces, tabs, and comments beginning with `#` are ignored. Strings use double quotes and support `\n`, `\t`, `\"`, and `\\` escapes. Identifiers begin with a letter or underscore and may include digits and underscores.

The frontend preserves source spans (start and end line/column positions) on syntax-tree nodes. Lexer, parser, and runtime errors use these spans to identify the relevant source location.

## Variables

`set name to expression` replaces the nearest existing binding with that name. If no enclosing environment contains the name, it defines a new variable in the current environment. This makes `set` both the initial declaration and reassignment form.

```clr
set score to 100
```

The nearest-binding rule remains in effect across block and function boundaries: assigning to an existing outer variable modifies it in the outer scope, whereas new variables created with `set` inside a function or block remain local.

## Output

`say expression` writes a value; parentheses are not required.

```clr
say "Score: " + score
```

## Expressions and operators

Grouping uses parentheses. Precedence from low to high is `or`, `and`, equality (`==`, `!=`), comparison (`>`, `<`, `>=`, `<=`), addition/subtraction, multiplication/division/remainder, then unary `not`, `-`, and `+`. Operators at the same precedence level associate from left to right.

Arithmetic operators require numbers (booleans are not numbers). `/` and `%` reject division by zero. `+` adds two numbers, or concatenates when either operand is a string after converting the other operand to its Clarity display form. Comparisons support two numbers or two strings only. Equality treats values of different Clarity types as unequal; in particular, `true == 1` is false.

`false` and `nothing` are falsey. All other current values, including `0`, empty strings, empty lists, and empty dictionaries, are truthy. `not` always returns a boolean. `and` and `or` short-circuit and always return a boolean.

## Data types

Numbers (integers and decimals), strings, booleans (`true`, `false`), null (`nothing` or `null`), lists, dictionaries, and functions are supported. `say` displays `nothing`, `true`, and `false` with these spellings; strings without quotes; lists/dictionaries using Clarity-style literals; and functions as `<function name>`.

## Lists

List literals use brackets. `push expression to listName` appends an item; `pop from listName` removes the final item. `pop`'s returned value is currently not assignable because assignments are the only supported variable update statement.

## Dictionaries

Dictionary literals use braces and colons: `{"name": "Creebrine", "age": 14}`. Keys may be numbers, strings, booleans, or `nothing`; list and dictionary keys are rejected. There is no dictionary access or mutation syntax yet.

## Blocks and lexical scope

A block is a brace-delimited sequence of statements: `{ ... }`. Whitespace and indentation are not significant. Blocks may be nested, may be empty, and create child lexical environments. Variables newly created with `set` inside a block do not exist after the block ends. `set` still updates the nearest existing binding, including one in an enclosing block or outer environment.

## Functions

Functions are declared with the `function` keyword followed by the function name, optional parameters, and a block body:

```clr
function greet {
    say "Hello"
}

function greet taking name {
    say "Hello, " + name
}

function add taking a and b {
    return a + b
}
```

### Parameters

Parameters are introduced with `taking` and chained with `and`:

```clr
function sum taking a and b and c {
    return a + b + c
}
```

Parameter names must be unique within a function declaration; duplicate parameter names produce a parser error. Parameters are local to the function invocation and shadow enclosing bindings of the same name.

### Function calls

Function calls use mandatory parentheses with comma-separated arguments:

```clr
greet()
greet("Creebrine")
add(10, 20)
```

Calls are expressions and can be used in expressions, variable assignments, or as standalone statements. Chained calls (e.g. `make_counter()()`) are supported. Calling a non-function or passing an incorrect number of arguments produces a runtime error.

### Return statements

Functions return values using the `return` statement:

```clr
return
return expression
```

* `return expression` evaluates the expression and immediately exits the function with that value.
* Bare `return` exits the function and produces `nothing`.
* Falling off the end of a function body without an explicit return also produces `nothing`.
* Using `return` outside of a function is a runtime error.

### Scope and closures

Each function call creates a new execution environment whose parent is the function's captured declaration environment (lexical closure).

Nested functions capture their surrounding environment, retaining access to outer variables even after the outer function finishes executing:

```clr
function make_adder taking x {
    function add taking y {
        return x + y
    }
    return add
}

set add5 to make_adder(5)
say add5(10) # 15
```

Each closure invocation operates on its captured environment; multiple instances of a closure maintain independent mutable state.

### Recursion

Functions can call themselves recursively, and multiple functions can be mutually recursive:

```clr
function factorial taking n {
    if n <= 1 {
        return 1
    }
    return n * factorial(n - 1)
}
```

### First-class functions

Functions are first-class values and can be:
* Assigned to variables (`set f to greet`)
* Called through variables (`f()`)
* Passed as arguments to other functions
* Returned from other functions
* Stored in lists and dictionaries

### Control-flow boundaries

Function calls establish a strict control-flow boundary:
* `break` affects only loops within the currently executing function. A `break` inside a function cannot exit or affect an outer caller's loop. Using `break` outside a loop inside a function is a runtime error.
* `continue` affects only loops within the currently executing function.
* `return` exits only the nearest enclosing function invocation, unwinding any active loops or blocks inside that function.

## If and else

`if` evaluates its condition using Clarity truthiness and executes its block only when the condition is truthy. `else if` chains additional conditions; only the first matching branch executes. `else` executes when no preceding branch matched.

```clr
if score >= 90 {
    say "Excellent!"
} else if score >= 70 {
    say "Good job!"
} else {
    say "Keep practicing!"
}
```

## While loops

`while condition { ... }` evaluates its condition before every iteration. Its body is a block and follows normal lexical-scope rules.

## For-in loops

`for name in expression { ... }` iterates over lists and strings. The loop variable is local to the loop and shadows any enclosing variable with the same name; an outer variable of that name is not changed by the iteration binding.

## Numeric range loops

`for name from start to end { ... }` visits every numeric value from start to end, including the endpoint. Direction is selected automatically: lower-to-higher ranges ascend and higher-to-lower ranges descend. An optional `step expression` controls the positive distance between values; its sign is ignored and it must not be zero.

```clr
for number from 10 to 1 step 2 {
    say number
}
```

## Break and continue

`break` exits the nearest enclosing `while`, `for-in`, or numeric range loop within the current function. `continue` skips to the next iteration of that nearest loop. Using either outside a loop is a runtime error.

## Comments

Use `#` for a line comment.

## Current limitations

There are no anonymous functions, default parameters, typed parameters, classes, modules, indexing, static analysis, formatter, package manager, or compilation backends. These are planned future capabilities and are not implemented in 0.3.0.
