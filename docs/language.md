# Clarity Language Guide

Clarity is designed to read like clear, structured English while maintaining strict computational predictability. This guide details the core syntax and runtime behaviors of Clarity 0.5.0.

---

## 1. Variables & Scope

Variables are assigned using `set name to value`:

```clr
set score to 100
set player to "Creebrine"
```

### Nearest-Binding Rule
Clarity resolves assignments by updating the nearest existing variable in enclosing lexical scopes. If the variable is not found in any enclosing scope, it is defined in the current local environment.

```clr
set global_counter to 0

function increment {
    set global_counter to global_counter + 1  # Modifies outer global_counter
}

increment()
say global_counter  # 1
```

---

## 2. Data Types & Values

Clarity provides seven core value types:

| Type | Examples | Description |
|---|---|---|
| **Number** | `42`, `-7`, `3.14159` | Integers and floating-point decimal numbers. |
| **String** | `"Hello"`, `"Café \n"` | UTF-8 text in double quotes with escape sequences (`\n`, `\t`, `\"`, `\\`). |
| **Boolean** | `true`, `false` | Logical truth values. Notice: `true != 1`. |
| **Null** | `nothing` (or `null`) | Absence of a value. |
| **List** | `[1, 2, "three"]` | Ordered, mutable sequence of values. |
| **Dictionary** | `{ name: "Alice", age: 30 }` | Key-value mapping preserving distinct key types. |
| **Function** | `<function greet>` | First-class callable code blocks and closures. |

### Truthiness
Only `false` and `nothing` are falsey. All other values—including `0`, `""`, `[]`, and `{}`—are truthy.

---

## 3. Operators & English Aliases

### Arithmetic Operators
* `+` : Numeric addition or string concatenation.
* `-` : Subtraction or unary negation.
* `*` : Multiplication.
* `/` : Division (raises runtime error on zero divisor).
* `%` : Remainder / modulo (raises runtime error on zero divisor).

### Comparison Operators & Aliases
Clarity allows you to write comparisons using either symbolic operators or readable English phrases:

| English Phrase | Operator | Example |
|---|---|---|
| `is equal to` | `==` | `a is equal to b` |
| `is not equal to` | `!=` | `a is not equal to b` |
| `is greater than` | `>` | `score is greater than 90` |
| `is less than` | `<` | `health is less than 20` |
| `is at least` | `>=` | `age is at least 18` |
| `is at most` | `<=` | `count is at most 10` |

### Logical Operators
* `and` : Short-circuiting logical conjunction.
* `or` : Short-circuiting logical disjunction.
* `not` : Logical negation (`not true` -> `false`).

---

## 4. Control Flow

### If / Else Conditionals
```clr
if score >= 90 {
    say "Grade: A"
} else if score is at least 80 {
    say "Grade: B"
} else {
    say "Keep practicing!"
}
```

### While Loops
```clr
set count to 3
while count > 0 {
    say count
    set count to count - 1
}
```

### For-Each Loops
Iterate over elements of a list or characters of a string:

```clr
set inventory to ["Sword", "Shield", "Potion"]

for each item in inventory {
    say "- " + item
}
```

### Numeric Range Loops
Iterates between endpoints inclusive, automatically selecting ascending or descending direction:

```clr
# Ascending
for i from 1 to 5 {
    say i
}

# Descending with step
for n from 10 to 0 step 2 {
    say n
}
```

### Repeat Loops
Executes a block a fixed number of times:

```clr
repeat 3 times {
    say "Hip hip hooray!"
}
```

### Loop Control
`break` exits the nearest enclosing loop. `continue` advances to the next iteration.

---

## 5. Functions & Closures

### Function Declarations
Functions are declared with `function` and optional parameter chains using `taking ... and ...`:

```clr
# Zero parameters
function greet {
    say "Hello, Clarity!"
}

# One parameter
function greet_user taking name {
    say "Hello, " + name
}

# Multiple parameters
function calculate_area taking width and height {
    return width * height
}
```

### Return Values
* `return value` exits the function and returns `value`.
* Bare `return` or falling off the end of a function returns `nothing`.

### Closures & First-Class Functions
Functions capture their enclosing environment at definition time:

```clr
function make_multiplier taking factor {
    function multiply taking number {
        return number * factor
    }
    return multiply
}

set double to make_multiplier(2)
say double(10)  # 20
```

---

## 6. Collections & Indexing

### Lists
```clr
set items to ["a", "b", "c"]

# 0-based indexing
say items[0]  # "a"

# Indexed assignment
set items[1] to "x"
say items     # ["a", "x", "c"]

# Push and pop statements
push "d" to items
set last to pop from items
```

### Dictionaries
```clr
set user to {
    name: "Creebrine",
    level: 42
}

say user["name"]     # "Creebrine"
set user["level"] to 43
```

### String Indexing
Strings support read-only 0-based indexing:

```clr
set word to "Clarity"
say word[0]  # "C"
```
