# Clarity Examples Guide

The repository includes runnable sample programs in the [`examples/`](../examples/) directory demonstrating various language and standard library capabilities.

You can run any example with:
```bash
clarity examples/<example_name>.clr
```

---

## 1. Hello World (`examples/hello.clr`)
Demonstrates basic output using the `say` statement.

```clr
say "Hello, Clarity!"
```
**Output**:
```text
Hello, Clarity!
```

---

## 2. Variables (`examples/variables.clr`)
Demonstrates variable declaration, assignment, and string concatenation.

```clr
set name to "Creebrine"
set age to 14

say "Name: " + name
say "Age: " + age
```
**Output**:
```text
Name: Creebrine
Age: 14
```

---

## 3. Calculator (`examples/calculator.clr`)
Demonstrates arithmetic operations and operator precedence.

```clr
set a to 10
set b to 20
set result to a + b

say result
```
**Output**:
```text
30
```

---

## 4. Control Flow (`examples/control_flow.clr`)
Demonstrates `if/else`, English comparison aliases (`is at least`), `while` loops, `for each` loops, and `repeat` loops with `break`/`continue`.

```clr
set score to 85

if score is at least 90 {
    say "Excellent!"
} else if score is at least 70 {
    say "Good job!"
} else {
    say "Keep trying!"
}

# While loop
set count to 0
while count < 3 {
    say "Count: " + count
    set count to count + 1
}

# For-each loop
set items to ["Sword", "Shield", "Potion"]
for each item in items {
    if item == "Shield" {
        continue
    }
    say "Item: " + item
}

# Range loop
for num from 1 to 5 step 2 {
    say num
}
```

---

## 5. Functions & Closures (`examples/functions.clr`)
Demonstrates function definitions with `taking`, parameters, return values, higher-order functions, and stateful closures.

```clr
function greet taking name {
    say "Hello, " + name
}

greet("Creebrine")

function add taking a and b {
    return a + b
}

say "Result: " + add(10, 20)

function make_counter {
    set count to 0
    function increment {
        set count to count + 1
        return count
    }
    return increment
}

set counter to make_counter()
say "Count: " + counter()
say "Count: " + counter()
```
**Output**:
```text
Hello, Creebrine
Result: 30
Count: 1
Count: 2
```

---

## 6. Data Access & Readability (`examples/data_access.clr`)
Demonstrates list indexing, dictionary indexing, nested indexing, indexed assignment, string indexing, and English comparison aliases.

```clr
set items to ["Sword", "Shield", "Potion"]
set items[1] to "Magic Shield"

set user to {
    name: "Creebrine",
    age: 14,
    scores: [95, 100]
}

say "User: " + user["name"]
set user["scores"][0] to 98

if user["age"] is at least 13 {
    say "Eligible for account"
}

repeat 3 times {
    say "Hooray!"
}
```

---

## 7. Standard Library (`examples/standard_library.clr`)
Demonstrates text manipulation (`trim`, `uppercase`, `split`, `join`), collections (`length`, `sort`, `reverse`, `min`, `max`), math (`sqrt`, `power`, `floor`, `ceil`, `round`), and random utilities (`random`, `choose`).

```clr
# Text Manipulation
set greeting to "  Welcome to Clarity  "
say "Trimmed & Uppercase: " + uppercase(trim(greeting))

set words to split("clarity,simplicity,elegance", ",")
say "Joined words: " + join(words, " -> ")

# Collections
set scores to [88, 42, 95, 70, 100]
say "Sorted scores: " + sort(scores)
say "Lowest score: " + min(scores)

# Math
say "Square root of 81: " + sqrt(81)
say "Power (2^8): " + power(2, 8)

# Random Selection
set roll to random(1, 6)
say "Rolled a die (1-6): " + roll
```
