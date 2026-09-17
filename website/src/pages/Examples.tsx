import React, { useState } from 'react';
import { CodeBlock } from '../components/CodeBlock';
import { SEO } from '../components/SEO';

interface ExampleItem {
  id: string;
  category: 'beginner' | 'features' | 'stdlib';
  title: string;
  filename: string;
  description: string;
  code: string;
  output: string;
}

const EXAMPLES: ExampleItem[] = [
  // Beginner
  {
    id: 'hello',
    category: 'beginner',
    title: 'Hello World',
    filename: 'hello.clr',
    description: 'The classic introductory program displaying text using the `say` statement.',
    code: `say "Hello, Clarity!"`,
    output: `Hello, Clarity!`,
  },
  {
    id: 'variables',
    category: 'beginner',
    title: 'Variables & String Concatenation',
    filename: 'variables.clr',
    description: 'Declaring variables with `set ... to ...` and concatenating strings.',
    code: `set name to "Creebrine"
set age to 14

say "Name: " + name
say "Age: " + age`,
    output: `Name: Creebrine\nAge: 14`,
  },
  {
    id: 'calculator',
    category: 'beginner',
    title: 'Simple Calculator',
    filename: 'calculator.clr',
    description: 'Arithmetic operations, variable assignments, and operator evaluation.',
    code: `set a to 10
set b to 20
set result to a + b

say result`,
    output: `30`,
  },

  // Language Features
  {
    id: 'control_flow',
    category: 'features',
    title: 'Control Flow & Loops',
    filename: 'control_flow.clr',
    description: 'Demonstrating `if/else`, English comparison aliases (`is at least`), `while`, `for each`, and `repeat` loops.',
    code: `set score to 85

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
set items to ["Sword", "Potion"]
for each item in items {
    say "Item: " + item
}

# Range loop
for num from 1 to 5 step 2 {
    say num
}`,
    output: `Good job!\nCount: 0\nCount: 1\nCount: 2\nItem: Sword\nItem: Potion\n1\n3\n5`,
  },
  {
    id: 'functions',
    category: 'features',
    title: 'Functions & Stateful Closures',
    filename: 'functions.clr',
    description: 'Function parameters with `taking`, return values, higher-order functions, and closures.',
    code: `function greet taking name {
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
say "Count: " + counter()`,
    output: `Hello, Creebrine\nResult: 30\nCount: 1\nCount: 2`,
  },
  {
    id: 'data_access',
    category: 'features',
    title: 'Data Access & Indexing',
    filename: 'data_access.clr',
    description: '0-based indexing on lists and dictionaries, nested indexed mutation, and repeat loops.',
    code: `set items to ["Sword", "Shield", "Potion"]
say "First item: " + items[0]

set items[1] to "Magic Shield"
say "Updated inventory: " + items

set user to {
    name: "Creebrine",
    age: 14,
    scores: [95, 100]
}

say "User: " + user["name"]
set user["age"] to 15
say "New age: " + user["age"]

# Nested Indexing
say "Top score: " + user["scores"][1]

# Repeat loop
repeat 3 times {
    say "Hooray!"
}`,
    output: `First item: Sword\nUpdated inventory: ["Sword", "Magic Shield", "Potion"]\nUser: Creebrine\nNew age: 15\nTop score: 100\nHooray!\nHooray!\nHooray!`,
  },

  // Standard Library
  {
    id: 'stdlib',
    category: 'stdlib',
    title: 'Standard Library Showcase',
    filename: 'standard_library.clr',
    description: 'Built-in functions for text manipulation, collection sorting, math utilities, and random selection.',
    code: `# 1. Text Manipulation
set greeting to "  Welcome to Clarity  "
say "Trimmed & Uppercase: " + uppercase(trim(greeting))

set words to split("clarity,simplicity,elegance", ",")
say "Joined words: " + join(words, " -> ")
say "Contains 'simplicity': " + contains(greeting, "Clarity")

# 2. Collections
set scores to [88, 42, 95, 70, 100]
say "Total scores: " + length(scores)
say "Sorted scores: " + sort(scores)
say "Lowest score: " + min(scores)
say "Highest score: " + max(scores)

# 3. Math
say "Square root of 81: " + sqrt(81)
say "Power (2^8): " + power(2, 8)
say "Floor of 7.9: " + floor(7.9)
say "Rounded 3.14159 to 2 digits: " + round(3.14159, 2)

# 4. Random Selection
set roll to random(1, 6)
say "Rolled a die (1-6): " + roll`,
    output: `Trimmed & Uppercase: WELCOME TO CLARITY\nJoined words: clarity -> simplicity -> elegance\nContains 'simplicity': true\nTotal scores: 5\nSorted scores: [42, 70, 88, 95, 100]\nLowest score: 42\nHighest score: 100\nSquare root of 81: 9\nPower (2^8): 256\nFloor of 7.9: 7\nRounded 3.14159 to 2 digits: 3.14\nRolled a die (1-6): 5`,
  },
];

export const Examples: React.FC = () => {
  const [filter, setFilter] = useState<'all' | 'beginner' | 'features' | 'stdlib'>('all');

  const filteredExamples =
    filter === 'all' ? EXAMPLES : EXAMPLES.filter((ex) => ex.category === filter);

  return (
    <div className="container" style={{ padding: '60px 24px 100px' }}>
      <SEO
        title="Clarity Examples"
        description="Explore real runnable Clarity 0.5.0 programs showcasing control flow, lexical closures, indexed data structures, and the standard library."
        canonicalPath="/examples"
      />
      <div style={{ textAlign: 'center', maxWidth: '640px', margin: '0 auto 48px' }}>
        <span className="badge" style={{ marginBottom: '12px' }}>
          Code Gallery
        </span>
        <h1 style={{ fontSize: '2.8rem', marginBottom: '16px' }}>Examples Showcase</h1>
        <p style={{ fontSize: '1.1rem', color: 'var(--text-secondary)' }}>
          Explore real runnable Clarity 0.5.0 programs from the official repository.
        </p>
      </div>

      {/* Filter Tabs */}
      <div
        style={{
          display: 'flex',
          flexWrap: 'wrap',
          gap: '10px',
          justifyContent: 'center',
          marginBottom: '48px',
        }}
      >
        {[
          { id: 'all', label: 'All Examples' },
          { id: 'beginner', label: 'Beginner' },
          { id: 'features', label: 'Language Features' },
          { id: 'stdlib', label: 'Standard Library' },
        ].map((tab) => {
          const active = filter === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setFilter(tab.id as any)}
              className={`btn ${active ? 'btn-primary' : 'btn-secondary'}`}
              style={{ padding: '8px 18px', fontSize: '0.9rem' }}
            >
              {tab.label}
            </button>
          );
        })}
      </div>

      {/* Grid of Examples */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))',
          gap: '32px',
        }}
      >
        {filteredExamples.map((ex) => (
          <div key={ex.id} style={{ display: 'flex', flexDirection: 'column' }}>
            <div style={{ marginBottom: '12px' }}>
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  marginBottom: '6px',
                }}
              >
                <h3 style={{ fontSize: '1.2rem', color: 'var(--text-primary)' }}>
                  {ex.title}
                </h3>
                <span
                  className="badge"
                  style={{
                    fontSize: '0.68rem',
                    textTransform: 'uppercase',
                  }}
                >
                  {ex.category}
                </span>
              </div>
              <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)' }}>
                {ex.description}
              </p>
            </div>

            <div style={{ flex: 1 }}>
              <CodeBlock
                code={ex.code}
                filename={ex.filename}
                output={ex.output}
                showLineNumbers={true}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
