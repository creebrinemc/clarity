# Clarity Standard Library Reference

Clarity 0.5.0 features a hybrid standard-library model. Core common utilities are **globally available** without imports, exposed as first-class callable values.

---

## 1. Text Functions

### `length(text)`
Returns the number of Unicode characters in `text`.

```clr
say length("Clarity")  # 7
say length("café")     # 4
```

### `uppercase(text)`
Returns `text` converted to uppercase.
* **Error**: Raises a runtime error if `text` is not a string.

```clr
say uppercase("hello")  # "HELLO"
```

### `lowercase(text)`
Returns `text` converted to lowercase.
* **Error**: Raises a runtime error if `text` is not a string.

```clr
say lowercase("WORLD")  # "world"
```

### `trim(text)`
Returns `text` with leading and trailing whitespace removed.
* **Error**: Raises a runtime error if `text` is not a string.

```clr
say trim("  spaced  ")  # "spaced"
```

### `contains(text, substring)`
Returns `true` if `substring` appears inside `text`, otherwise `false`.
* **Error**: Raises a runtime error if `substring` is not a string.

```clr
say contains("Hello World", "World")  # true
```

### `replace(text, old, new)`
Returns a new string with all occurrences of `old` replaced by `new`.
* **Error**: Raises a runtime error if any argument is not a string.

```clr
say replace("banana", "a", "o")  # "bonono"
```

### `split(text, separator)`
Splits `text` by `separator` and returns a list of strings.
* **Error**: Raises a runtime error if `separator` is empty or arguments are not strings.

```clr
say split("red,green,blue", ",")  # ["red", "green", "blue"]
```

### `join(items, separator)`
Joins the elements of `items` into a single string using `separator`.
* Non-string elements in `items` are converted to their Clarity string representation.
* **Error**: Raises a runtime error if `items` is not a list or `separator` is not a string.

```clr
say join(["a", "b", "c"], "-")  # "a-b-c"
```

---

## 2. Collection Functions

### `length(collection)`
Returns the number of elements in a list, entries in a dictionary, or characters in a string.

```clr
say length([10, 20, 30])                # 3
say length({ name: "Creebrine", age: 14 }) # 2
```

### `contains(collection, value)`
* **Lists**: Returns `true` if any element equals `value` using Clarity type-strict equality (`1 != true`).
* **Dictionaries**: Returns `true` if `value` exists as a dictionary key.

```clr
say contains(["a", "b"], "a")     # true
say contains([1, 2], true)        # false (distinct types)
say contains({ score: 100 }, "score") # true
```

### `reverse(collection)`
Returns a new reversed copy of a list or string. The original collection is **not mutated**.

```clr
set numbers to [1, 2, 3]
set rev to reverse(numbers)
say rev      # [3, 2, 1]
say numbers  # [1, 2, 3] (original intact)
```

### `sort(collection)`
Returns a new sorted copy of a list. The original list is **not mutated**.
* Elements must be all numbers (sorted numerically) or all strings (sorted lexicographically).
* **Error**: Raises a runtime error if elements have mixed or unsupported types.

```clr
say sort([4, 1, 3, 2])              # [1, 2, 3, 4]
say sort(["banana", "apple", "cherry"]) # ["apple", "banana", "cherry"]
```

---

## 3. Math Functions

### `abs(number)`
Returns the absolute value of `number`, preserving integer or floating-point type.

```clr
say abs(-15)    # 15
say abs(-3.14)  # 3.14
```

### `floor(number)`
Returns the largest integer less than or equal to `number`.

```clr
say floor(4.9)   # 4
say floor(-4.1)  # -5
```

### `ceil(number)`
Returns the smallest integer greater than or equal to `number`.

```clr
say ceil(4.1)   # 5
say ceil(-4.9)  # -4
```

### `round(number [, digits])`
Rounds `number` to the nearest integer, or to `digits` decimal places if specified.

```clr
say round(3.7)       # 4
say round(3.14159, 2) # 3.14
```

### `min(...)` & `max(...)`
Accepts either multiple scalar arguments (e.g. `min(10, 5, 20)`) or a single list (e.g. `min([10, 5, 20])`).
* All compared values must be all numbers or all strings.
* **Error**: Raises a runtime error on empty lists or mixed types.

```clr
say min(10, 20, 5)        # 5
say max([100, 42, 350])   # 350
say min("apple", "zebra") # "apple"
```

### `sqrt(number)`
Returns the square root of `number`.
* Returns an exact integer if `number` is an integer perfect square.
* **Error**: Raises a runtime error if `number` is negative.

```clr
say sqrt(25)  # 5
say sqrt(2)   # 1.4142135623730951
```

### `power(base, exponent)`
Returns `base` raised to `exponent`.
* **Error**: Raises a runtime error on division by zero (`power(0, -1)`) or complex fractional powers of negative bases.

```clr
say power(2, 8)  # 256
say power(4, 0.5) # 2.0
```

---

## 4. Random Functions

### `random(minimum, maximum)`
* If both bounds are integers: returns a random integer in `[minimum, maximum]` inclusive.
* If either bound is a float: returns a uniform random float in `[minimum, maximum]`.
* **Error**: Raises a runtime error if `minimum > maximum`.

```clr
set dice to random(1, 6)
set rate to random(0.0, 1.0)
```

### `choose(items)`
Randomly returns an element from a non-empty list or string.
* **Error**: Raises a runtime error if `items` is empty or not a collection.

```clr
set fruit to choose(["apple", "banana", "cherry"])
set char to choose("Clarity")
```

---

## 5. File Operations

### `read_file(path)`
Reads and returns the contents of a UTF-8 text file.
* **Error**: Raises a Clarity runtime error if the file does not exist, is a directory, or fails to decode.

```clr
set content to read_file("config.txt")
```

### `write_file(path, content)`
Writes `content` to `path` using UTF-8 encoding. Automatically creates parent directories if needed. Returns `nothing`.
* **Error**: Raises a Clarity runtime error if writing fails or path is a directory.

```clr
write_file("output/data.txt", "Saved state")
```

### `file_exists(path)`
Returns `true` if a file or directory exists at `path`, otherwise `false`.

```clr
if file_exists("output/data.txt") {
    say "File found!"
}
```

---

## 6. First-Class Standard Library Functions

All standard-library functions can be assigned to variables, passed to other functions, or returned from closures:

```clr
set op to uppercase
say op("hello")  # "HELLO"

function apply taking func and value {
    return func(value)
}

say apply(sqrt, 100)  # 10
```
