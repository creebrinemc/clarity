# Clarity 0.6.0 Specification

## Language philosophy

Clarity aims for readable, English-inspired syntax while keeping common code concise. Version 0.5.0 introduced a globally available standard library covering text manipulation, collection utilities, math functions, random selection, and file operations. Version 0.6.0 adds modules and imports, dot member access, static project manifests (`conf.clr`), a project-aware CLI (`clarity run`, `clarity new`, `clarity test`), and assertion built-ins for native tests.

## Standard Library

Clarity uses a hybrid standard-library model:
- Common/core functionality is globally available without imports (e.g. `length`, `sqrt`, `uppercase`, `random`).
- User code is organized into modules with `import` / `from ... import` (see [Modules and imports](#modules-and-imports)). Standard-library functions remain global in 0.6.0; namespaced standard-library modules are a future capability.

Standard library functions are first-class callable values, printable as `<function name>`, assignable to variables, and passable to higher-order functions. Standard library errors produce proper Clarity runtime errors with source spans and never leak raw host exceptions.

### Text Functions

* `length(value)`: Returns the integer number of characters in a string, items in a list, or key-value entries in a dictionary.
* `uppercase(text)`: Returns a new string with all characters converted to uppercase. Requires a string argument.
* `lowercase(text)`: Returns a new string with all characters converted to lowercase. Requires a string argument.
* `trim(text)`: Returns a new string with leading and trailing whitespace removed. Requires a string argument.
* `contains(text, substring)`: Returns `true` if `substring` is found inside `text`, otherwise `false`. Both arguments must be strings.
* `replace(text, old, new)`: Returns a new string with all occurrences of `old` replaced by `new`. All three arguments must be strings.
* `split(text, separator)`: Splits `text` by `separator` and returns a Clarity list of strings. `separator` cannot be empty.
* `join(items, separator)`: Joins elements of the `items` list into a string separated by `separator`. Non-string elements in `items` are converted to their Clarity display form.

```clr
set name to "  Creebrine  "
say uppercase(trim(name))               # "CREEBRINE"
say contains(name, "Cree")             # true
say replace("banana", "a", "o")        # "bonono"
say split("a,b,c", ",")                # ["a", "b", "c"]
say join(["one", "two", "three"], "-") # "one-two-three"
```

### Collection Utilities

* `length(collection)`: Returns the number of items in a list, dictionary, or string.
* `contains(collection, value)`:
  * For lists: returns `true` if any element matches `value` using Clarity equality (`1 != true`).
  * For dictionaries: returns `true` if `value` exists as a key in the dictionary.
* `reverse(collection)`: Returns a new reversed copy of a list or string. The original collection is not mutated.
* `sort(collection)`: Returns a new sorted copy of a list. The original list is not mutated.
  * All elements must be numbers (sorted numerically) or all elements must be strings (sorted lexicographically).
  * Lists with mixed types or unsupported element types produce a Clarity runtime error.

```clr
set items to [4, 1, 3, 2]
say sort(items)     # [1, 2, 3, 4]
say reverse(items)  # [2, 3, 1, 4]
say items           # [4, 1, 3, 2] (unchanged)
```

### Math Functions

* `abs(number)`: Returns the absolute value of a number. Preserves integer or decimal types.
* `floor(number)`: Returns the largest integer less than or equal to `number`.
* `ceil(number)`: Returns the smallest integer greater than or equal to `number`.
* `round(number [, digits])`: Rounds `number` to the nearest integer, or to `digits` decimal places if `digits` is specified.
* `min(...)`: Returns the minimum value. Accepts either multiple arguments (e.g. `min(1, 2, 3)`) or a single list (e.g. `min([1, 2, 3])`). All values must be numbers or all strings.
* `max(...)`: Returns the maximum value. Accepts either multiple arguments or a single list.
* `sqrt(number)`: Returns the square root of `number`. Returns an exact integer if `number` is an integer perfect square, otherwise a float. Negative numbers produce a runtime error.
* `power(base, exponent)`: Returns `base` raised to `exponent`. Division by zero in negative exponents or fractional powers of negative numbers produce a runtime error.

```clr
say sqrt(25)        # 5
say power(2, 8)     # 256
say min(10, 5, 20)  # 5
say max([1, 99, 4]) # 99
```

### Random Functions

* `random(minimum, maximum)`:
  * If both `minimum` and `maximum` are integers, returns a random integer in `[minimum, maximum]` inclusive.
  * If either bound is a decimal, returns a random uniform float in `[minimum, maximum]`.
  * If `minimum > maximum`, a runtime error is raised.
* `choose(items)`: Returns a randomly selected element from a non-empty list or string. Empty collections produce a runtime error.

```clr
set roll to random(1, 6)
set pick to choose(["apple", "banana", "cherry"])
```

### File Operations

* `read_file(path)`: Reads a text file using UTF-8 encoding. Nonexistent files or read errors produce a Clarity runtime error.
* `write_file(path, content)`: Writes string `content` to `path` using UTF-8 encoding. Creates parent directories if needed. Returns `nothing`.
* `file_exists(path)`: Returns `true` if a file or directory exists at `path`, otherwise `false`.

```clr
write_file("data.txt", "Hello Clarity!")
if file_exists("data.txt") {
    say read_file("data.txt")
}
```

Filesystem operations are abstracted to allow pluggable backends and sandboxed implementations for browser playgrounds.

### Testing and Assertion Functions

* `assert(condition [, message])`: Does nothing if `condition` is truthy. Otherwise raises a Clarity runtime error `Assertion failed: <message>` (default message: `Assertion failed`).
* `assert_equal(actual, expected [, message])`: Does nothing if `actual` and `expected` are equal under Clarity equality (so `1` and `true` are not equal). Otherwise raises a Clarity runtime error showing the optional message and the expected and actual values.

```clr
assert(10 > 5, "Ten should be greater than five")
assert_equal(2 * 3, 6, "2 times 3 is 6")
```

---

## Lexical structure

Source is line-oriented. Spaces, tabs, and comments beginning with `#` are ignored. Strings use double quotes and support `\n`, `\t`, `\"`, and `\\` escapes. Identifiers begin with a letter or underscore and may include digits and underscores. The period `.` is a token used for member access; inside numeric literals such as `3.14` it remains part of the number.

Reserved keywords: `set`, `to`, `say`, `push`, `pop`, `from`, `and`, `or`, `not`, `if`, `else`, `while`, `for`, `in`, `step`, `break`, `continue`, `function`, `taking`, `return`, `each`, `repeat`, `times`, `is`, `equal`, `greater`, `less`, `than`, `at`, `least`, `most`, `import`, `as`, plus the literal words `true`, `false`, `nothing`, and `null`. `import` and `as` became reserved in 0.6.0 and can no longer be used as identifiers.

The frontend preserves source spans (start and end line/column positions) on syntax-tree nodes. Lexer, parser, and runtime errors use these spans to identify the relevant source location.

## Variables and assignments

`set name to expression` replaces the nearest existing binding with that name. If no enclosing environment contains the name, it defines a new variable in the current environment.

```clr
set score to 100
```

`set target[index] to expression` updates an element in a mutable collection (list or dictionary), including arbitrarily nested targets:

```clr
set items[0] to "First"
set user["age"] to 15
set data["users"][0]["name"] to "Alice"
```

The nearest-binding rule remains in effect across block and function boundaries: assigning to an existing outer variable modifies it in the outer scope, whereas new variables created with `set` inside a function or block remain local.

## Output

`say expression` writes a value; parentheses are not required.

```clr
say "Score: " + score
```

## Expressions and operators

Grouping uses parentheses. Precedence from low to high is `or`, `and`, equality (`==`, `!=`, `is equal to`, `is not equal to`), comparison (`>`, `<`, `>=`, `<=`, `is greater than`, `is less than`, `is at least`, `is at most`), addition/subtraction, multiplication/division/remainder, unary `not`, `-`, and `+`, then postfix function calls `(...)`, indexing `[...]`, and member access `.name`.

Arithmetic operators require numbers (booleans are not numbers). `/` and `%` reject division by zero. `+` adds two numbers, or concatenates when either operand is a string after converting the other operand to its Clarity display form. Comparisons support two numbers or two strings only. Equality treats values of different Clarity types as unequal; in particular, `true == 1` is false.

`false` and `nothing` are falsey. All other current values, including `0`, empty strings, empty lists, and empty dictionaries, are truthy. `not` always returns a boolean. `and` and `or` short-circuit and always return a boolean.

### Comparison aliases

Clarity provides English comparison aliases identical in precedence and semantics to their symbolic counterparts:

| English Alias | Symbolic Operator | Description |
|---|---|---|
| `is equal to` | `==` | Equality |
| `is not equal to` | `!=` | Inequality |
| `is greater than` | `>` | Strictly greater than |
| `is less than` | `<` | Strictly less than |
| `is at least` | `>=` | Greater than or equal to |
| `is at most` | `<=` | Less than or equal to |

```clr
if age is at least 18 {
    say "Adult"
}
```

## Data types

Numbers (integers and decimals), strings, booleans (`true`, `false`), null (`nothing` or `null`), lists, dictionaries, functions, and modules are supported. `say` displays `nothing`, `true`, and `false` with these spellings; strings without quotes; lists/dictionaries using Clarity-style literals; and functions as `<function name>`.

## Lists and indexing

List literals use brackets: `[1, 2, 3]`.

* `push expression to listName` appends an item.
* `pop from listName` removes the final item.
* `list[index]` retrieves an element by 0-based integer index.
* `set list[index] to value` updates an element by 0-based integer index.

Indexes must be integers (floats with fractional parts, booleans, strings, and other types are rejected). Out-of-range indexes produce a runtime error.

```clr
set items to ["a", "b", "c"]
say items[0]         # "a"
set items[1] to "x"  # items becomes ["a", "x", "c"]
```

## Dictionaries and indexing

Dictionary literals use braces and colons: `{ name: "Creebrine", age: 14 }`.

* Keys in literals can be unquoted identifiers (treated as string keys), numbers, strings, booleans, or `nothing`.
* `dict[key]` retrieves the value for a key. If the key does not exist, a runtime error is raised.
* `set dict[key] to value` updates an existing key or adds a new key-value pair.
* List and dictionary keys are rejected.

```clr
set user to {
    name: "Creebrine",
    age: 14
}

say user["name"]
set user["age"] to 15
```

### Dot member access on dictionaries

`dict.name` is read-only shorthand for `dict["name"]` when the key is a string that is a valid identifier. A missing key raises a runtime error (`Property 'name' not found in dictionary`). Dot access on values other than dictionaries and modules raises a runtime error. Assignment through dot access (`set user.age to 15`) is not supported in 0.6.0; use indexed assignment.

```clr
say user.name     # same as user["name"]
```

## String indexing

Strings support 0-based integer indexing: `string[index]` returns a single-character string.

Strings are immutable; attempting indexed assignment on a string (`set string[index] to value`) produces a runtime error. Out-of-range indexes produce a runtime error.

```clr
set word to "Clarity"
say word[0]  # "C"
```

## Nested indexing

Indexing and calls can be chained arbitrarily:

```clr
say data["users"][0]["scores"][1]
set data["users"][0]["name"] to "Alicia"
```

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

Each function call creates a new execution environment whose parent is the function's captured declaration environment (lexical closure). Nested functions capture their surrounding environment, retaining access to outer variables even after the outer function finishes executing. Multiple instances of a closure maintain independent mutable state.

### Recursion

Functions can call themselves recursively, and multiple functions can be mutually recursive.

### First-class functions

Functions are first-class values and can be assigned to variables, passed as arguments, returned from other functions, and stored in lists and dictionaries.

### Control-flow boundaries

Function calls establish a strict control-flow boundary: `break` and `continue` affect only loops within the currently executing function; `return` exits only the nearest enclosing function invocation.

## If and else

`if` evaluates its condition using Clarity truthiness and executes its block only when the condition is truthy. `else if` chains additional conditions; only the first matching branch executes. `else` executes when no preceding branch matched.

```clr
if score >= 90 {
    say "Excellent!"
} else if score is at least 70 {
    say "Good job!"
} else {
    say "Keep practicing!"
}
```

## While loops

`while condition { ... }` evaluates its condition before every iteration. Its body is a block and follows normal lexical-scope rules.

## For-in and For-each loops

`for name in expression { ... }` and `for each name in expression { ... }` iterate over lists and strings. The loop variable is local to the loop and shadows any enclosing variable with the same name. Both forms are semantically identical.

```clr
for each item in inventory {
    say item
}
```

## Numeric range loops

`for name from start to end { ... }` visits every numeric value from start to end, including the endpoint. Direction is selected automatically: lower-to-higher ranges ascend and higher-to-lower ranges descend. An optional `step expression` controls the positive distance between values; its sign is ignored and it must not be zero.

```clr
for number from 10 to 1 step 2 {
    say number
}
```

## Repeat loops

`repeat count times { ... }` executes its body block `count` times.

* `count` must evaluate to a number.
* If `count` is zero or negative, the loop executes zero times.
* The loop body executes in a block scope and supports `break` and `continue`.

```clr
repeat 3 times {
    say "Hello!"
}
```

## Break and continue

`break` exits the nearest enclosing `while`, `for`, `for each`, `repeat`, or numeric range loop within the current function. `continue` skips to the next iteration of that nearest loop. Using either outside a loop is a runtime error.

## Comments

Use `#` for a line comment.

## Modules and imports

Every `.clr` file is a module. Modules are imported using quoted path strings.

### Import forms

```clr
import "utils/formatting" as fmt              # whole-module import; alias is required
from "utils/formatting" import format_name    # named import
from "math_helpers" import square, cube        # several names, comma-separated
from "math_helpers" import square and cube     # 'and' is accepted as a separator
from "math_helpers" import square as sq        # per-name alias
```

* `import "path" as alias` binds the module value to `alias`. Members are read with `alias.member`. Omitting `as alias` is a parser error.
* `from "path" import name [as alias], ...` binds each requested export directly. Requesting a name the module does not export raises a runtime error that lists the available exports.
* Import statements may appear anywhere a statement is allowed. They bind names using the same rule as `set` (the nearest existing binding is replaced; otherwise a new binding is created in the current scope).

### Exports and privacy

A module's exports are all bindings created at its top level, including functions, variables, and names it imported itself. Names beginning with `_` are private: importing or accessing them from another module raises a runtime error. Standard-library functions are not exports.

### Module resolution

A trailing `.clr` in the path is optional, and `\` is normalized to `/`. For a path `P`, each search location is tried as `P.clr`, then `P/main.clr`, then `P/mod.clr`:

1. **Relative paths** (beginning with `./` or `../`) are resolved only against the directory of the importing file. If none of the candidates exist, a module error is raised.
2. **Other paths** are searched in order:
   1. inside the project root, when the program belongs to a project: `src/P.clr`, `P.clr`, `src/P/main.clr`, `src/P/mod.clr`, `P/main.clr`, `P/mod.clr`;
   2. relative to the importing file's directory;
   3. relative to the current working directory.

If no candidate exists, a `Clarity Module Error` lists every searched location.

### Evaluation and caching

A module is evaluated once per program run, in its own isolated top-level scope that sees only the standard library. Later imports of the same file (by canonical path) reuse the cached module, so top-level side effects such as `say` run only on first import. Import cycles are detected and reported as a `Clarity Circular Import Error` showing the cycle chain (for example `b2.clr -> b1.clr -> b2.clr`).

### Dot member access on modules

`module.member` returns an export of the module. Accessing a private (`_`-prefixed) or missing member raises a runtime error.

## Projects

### The `conf.clr` manifest

A project is a directory containing a `conf.clr` file. `conf.clr` uses Clarity syntax but is never executed: it is parsed and validated statically. It must contain exactly one statement, `set project to { ... }`, whose value is a dictionary made only of literal values (strings, numbers, booleans, `nothing`, lists, and dictionaries). Expressions, function calls, and variables are rejected with a `Clarity Project Error`.

```clr
set project to {
    name: "my-app",
    version: "0.1.0",
    entry: "src/main.clr",
    description: "A Clarity project",
    author: "",
    license: "MIT"
}
```

| Field | Required | Rules |
|---|---|---|
| `name` | Yes | Non-empty; letters, digits, `_`, and `-` only. |
| `version` | Yes | A Semantic Versioning string, e.g. `"0.1.0"`. |
| `entry` | No | Path to the entry file, relative to the project root. If omitted: `src/main.clr` if it exists, else `main.clr` if it exists, else `src/main.clr` if a `src/` directory exists, else `main.clr`. |
| `description`, `author`, `license` | No | Informational strings. |
| `dependencies` | No | Accepted and stored, but not used in 0.6.0. Reserved for future package management. |

Other keys are accepted and ignored.

### Project root discovery

The project root is the nearest directory, starting from the relevant directory and moving upward, that contains `conf.clr`. The project root enables project-root module resolution.

## Command-line interface

| Command | Behavior |
|---|---|
| `clarity <file.clr>` | Runs a single file (script mode). If the file is inside a project, that project's root is used for module resolution. |
| `clarity run [entry]` | Runs `entry` if given; otherwise the `entry` of the nearest project. Without a project it falls back to `./src/main.clr`, then `./main.clr`. |
| `clarity new <name>` | Creates `<name>/` containing `conf.clr`, `README.md`, `src/main.clr`, and `tests/main_test.clr`. The target directory must not exist or must be empty. |
| `clarity test [path]` | Runs native tests (see below). |
| `clarity help [command]` | Prints help for the CLI or a command. |
| `clarity --version`, `-v` | Prints `Clarity 0.6.0`. |

Exit codes: `0` success; `1` a Clarity error (lexer, parser, runtime, module, file read error) or a failed test; `2` command-line usage errors and project errors such as a missing project, a missing configured entry file, or an invalid project name.

### Native test runner

`clarity test` searches recursively for files named `*_test.clr` or `test_*.clr`. It looks in the given `path` (a single `.clr` file path runs just that file). Without a path it uses the project's `tests/` directory, otherwise `./tests`, otherwise the current directory.

Each test file is run in its own scope, and its top-level output is suppressed. Then every top-level function whose name starts with `test_` is called with no arguments, in alphabetical order. A test passes if it finishes without a Clarity error. A file that defines no `test_` functions counts as a single test that passes if its top level runs without error. The command exits with `0` if all tests pass (including when no test files are found) and `1` otherwise.

## Current limitations

There are no anonymous functions, default parameters, typed parameters, classes, static analysis, formatter, linter, package manager, or compilation backends. Standard-library functions are not namespaced into modules, dot access is read-only, and `dependencies` in `conf.clr` is not resolved. These are planned future capabilities and are not implemented in 0.6.0.
