# Getting Started with Clarity

Welcome to Clarity! This guide walks you through setting up the Clarity development environment and running your first `.clr` program.

---

## 1. Prerequisites

Clarity 0.5.0 is currently distributed as a Python-based implementation. You will need:
* **Python**: 3.11 or newer
* **pip**: Standard Python package manager
* **git**: Optional, for cloning the repository

---

## 2. Installation & Setup

Clone the repository and install Clarity in editable mode with development dependencies:

```bash
git clone https://github.com/creebrinemc/clarity.git
cd clarity

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Clarity and test tools
pip install -e ".[dev]"
```

Verify your installation:

```bash
clarity --version
# Output: Clarity 0.5.0
```

You can also invoke the CLI directly using the Python module syntax:

```bash
python -m clarity.cli --version
```

---

## 3. Your First Program

Create a file named `welcome.clr`:

```clr
# welcome.clr
set name to "Explorer"
say "Hello, " + name + "! Welcome to Clarity."

function calculate_bonus taking base_score {
    if base_score is at least 100 {
        return base_score * 1.5
    }
    return base_score
}

set score to 120
say "Final score: " + calculate_bonus(score)
```

Run your program:

```bash
clarity welcome.clr
```

Output:
```text
Hello, Explorer! Welcome to Clarity.
Final score: 180.0
```

---

## 4. Basic Syntax Cheatsheet

### Variables
```clr
set count to 10
set name to "Clarity"
set is_ready to true
```

### Collections & Indexing
```clr
set items to ["Sword", "Shield", "Potion"]
say items[0]              # "Sword"
set items[1] to "Armor"

set player to { name: "Creebrine", score: 99 }
say player["name"]        # "Creebrine"
```

### English Comparison Phrases
```clr
if count is greater than 5 {
    say "Large batch"
}

if count is at most 10 {
    say "Within limits"
}
```

### Functions
```clr
function add taking a and b {
    return a + b
}

say add(10, 25) # 35
```

### Loops
```clr
# For-each loop
for each item in items {
    say item
}

# Range loop
for i from 1 to 5 {
    say i
}

# Repeat loop
repeat 3 times {
    say "Clarity!"
}
```

### Standard Library
```clr
say uppercase("hello")        # "HELLO"
say sqrt(64)                  # 8
say sort([5, 1, 9, 3])        # [1, 3, 5, 9]
say random(1, 100)            # Random integer 1..100
```

---

## 5. Next Steps

* Read the [Language Guide](language.md) for an in-depth tour of syntax and features.
* Explore the [Standard Library Reference](standard-library.md) for available built-in functions.
* Check out runnable programs in the [`examples/`](../examples/) directory.
* Read [SPEC.md](../SPEC.md) for the complete language specification.
