import React, { useState, useEffect } from 'react';
import { useLocation, Link } from 'react-router-dom';
import {
  BookOpen,
  Code2,
  Layers,
  Sparkles,
  Terminal,
  FileText,
  ChevronRight,
  ArrowLeft,
  ArrowRight,
} from 'lucide-react';
import { CodeBlock } from '../components/CodeBlock';
import { SEO } from '../components/SEO';
import { NotFound } from './NotFound';

interface DocSection {
  id: string;
  title: string;
  description: string;
  icon: React.ReactNode;
  content: React.ReactNode;
}

const VALID_SECTIONS = ['getting-started', 'language', 'standard-library', 'examples', 'ecosystem', 'spec'];

export const Docs: React.FC = () => {
  const location = useLocation();
  const rawPath = location.pathname.replace(/^\/docs\/?/, '').trim();
  const isInvalidSection = rawPath !== '' && !VALID_SECTIONS.includes(rawPath);
  const [activeTab, setActiveTab] = useState<string>('getting-started');

  useEffect(() => {
    if (rawPath && VALID_SECTIONS.includes(rawPath)) {
      setActiveTab(rawPath);
    } else if (!rawPath) {
      setActiveTab('getting-started');
    }
  }, [rawPath]);

  if (isInvalidSection) {
    return <NotFound />;
  }

  const sections: DocSection[] = [
    {
      id: 'getting-started',
      title: 'Getting Started',
      description: 'Step-by-step instructions for installing Clarity and running your first .clr script.',
      icon: <Terminal size={17} />,
      content: (
        <div>
          <div style={{ marginBottom: '28px' }}>
            <span className="badge" style={{ marginBottom: '8px' }}>Setup Guide</span>
            <h1 style={{ fontSize: '2.4rem', marginBottom: '12px' }}>Getting Started with Clarity</h1>
            <p style={{ fontSize: '1.1rem', color: 'var(--text-secondary)' }}>
              Step-by-step instructions for installing Clarity and running your first `.clr` script.
            </p>
          </div>

          <h2 style={{ fontSize: '1.5rem', marginTop: '32px', marginBottom: '16px' }}>1. Prerequisites</h2>
          <p style={{ marginBottom: '16px' }}>
            Clarity 0.5.0 is currently distributed as a pure Python-based interpreter prototype. You will need:
          </p>
          <ul style={{ paddingLeft: '24px', marginBottom: '24px', color: 'var(--text-secondary)' }}>
            <li><strong>Python</strong>: Version 3.11 or newer</li>
            <li><strong>pip</strong>: Python package manager</li>
          </ul>

          <h2 style={{ fontSize: '1.5rem', marginTop: '32px', marginBottom: '16px' }}>2. Installation & Verification</h2>
          <p style={{ marginBottom: '16px' }}>
            Clone the official repository and install Clarity in editable mode with development dependencies:
          </p>
          <CodeBlock
            code={`git clone https://github.com/creebrinemc/clarity.git
cd clarity

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate

# Install in editable mode
pip install -e ".[dev]"`}
            filename="terminal"
            showLineNumbers={false}
          />

          <p style={{ marginTop: '20px', marginBottom: '12px' }}>
            Verify that Clarity is properly installed:
          </p>
          <CodeBlock
            code={`clarity --version
# Output: Clarity 0.5.0`}
            filename="terminal"
            showLineNumbers={false}
          />

          <h2 style={{ fontSize: '1.5rem', marginTop: '36px', marginBottom: '16px' }}>3. Your First Program</h2>
          <p style={{ marginBottom: '16px' }}>
            Create a new file named <code>welcome.clr</code> with the following code:
          </p>
          <CodeBlock
            code={`# welcome.clr
set user to "Explorer"
say "Hello, " + user + "! Welcome to Clarity."

function compute_bonus taking base_score {
    if base_score is at least 100 {
        return base_score * 1.5
    }
    return base_score
}

set final_score to compute_bonus(120)
say "Your score: " + final_score`}
            filename="welcome.clr"
            output={`Hello, Explorer! Welcome to Clarity.\nYour score: 180.0`}
          />

          <p style={{ marginTop: '20px', marginBottom: '12px' }}>
            Execute the program via the CLI:
          </p>
          <CodeBlock
            code={`clarity welcome.clr`}
            filename="terminal"
            showLineNumbers={false}
          />
        </div>
      ),
    },
    {
      id: 'language',
      title: 'Language Guide',
      description: 'Detailed overview of Clarity syntax, variables, scoping, control flow, functions, and data structures.',
      icon: <Code2 size={17} />,
      content: (
        <div>
          <div style={{ marginBottom: '28px' }}>
            <span className="badge" style={{ marginBottom: '8px' }}>Core Language</span>
            <h1 style={{ fontSize: '2.4rem', marginBottom: '12px' }}>Language Guide</h1>
            <p style={{ fontSize: '1.1rem', color: 'var(--text-secondary)' }}>
              Detailed overview of Clarity syntax, variables, scoping, control flow, functions, and data structures.
            </p>
          </div>

          <h2 style={{ fontSize: '1.5rem', marginTop: '32px', marginBottom: '16px' }}>1. Variables & Scope</h2>
          <p style={{ marginBottom: '14px' }}>
            Variables are defined or updated with <code>set name to value</code>. Clarity enforces a <strong>nearest-binding rule</strong>: assignments modify the nearest existing variable in enclosing scopes. If none exists, it is created in the local scope.
          </p>
          <CodeBlock
            code={`set global_count to 0

function increment {
    set global_count to global_count + 1  # Updates outer variable
}

increment()
say global_count  # 1`}
            filename="scope.clr"
          />

          <h2 style={{ fontSize: '1.5rem', marginTop: '36px', marginBottom: '16px' }}>2. Data Types</h2>
          <p style={{ marginBottom: '16px' }}>
            Clarity provides seven core value types with strict equality semantics:
          </p>
          <div style={{ overflowX: 'auto', marginBottom: '24px' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.92rem' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid var(--border-medium)', color: 'var(--text-primary)' }}>
                  <th style={{ padding: '10px 14px' }}>Type</th>
                  <th style={{ padding: '10px 14px' }}>Examples</th>
                  <th style={{ padding: '10px 14px' }}>Semantics</th>
                </tr>
              </thead>
              <tbody style={{ color: 'var(--text-secondary)' }}>
                <tr style={{ borderBottom: '1px solid var(--border-subtle)' }}>
                  <td style={{ padding: '10px 14px', color: 'var(--accent)' }}>Number</td>
                  <td style={{ padding: '10px 14px' }}><code>42</code>, <code>-7</code>, <code>3.14159</code></td>
                  <td style={{ padding: '10px 14px' }}>Integers and floating-point decimals.</td>
                </tr>
                <tr style={{ borderBottom: '1px solid var(--border-subtle)' }}>
                  <td style={{ padding: '10px 14px', color: 'var(--accent)' }}>String</td>
                  <td style={{ padding: '10px 14px' }}><code>"Hello"</code>, <code>"Café"</code></td>
                  <td style={{ padding: '10px 14px' }}>UTF-8 text with escapes (<code>\n</code>, <code>\t</code>).</td>
                </tr>
                <tr style={{ borderBottom: '1px solid var(--border-subtle)' }}>
                  <td style={{ padding: '10px 14px', color: 'var(--accent)' }}>Boolean</td>
                  <td style={{ padding: '10px 14px' }}><code>true</code>, <code>false</code></td>
                  <td style={{ padding: '10px 14px' }}>Distinct from numbers (<code>true != 1</code>).</td>
                </tr>
                <tr style={{ borderBottom: '1px solid var(--border-subtle)' }}>
                  <td style={{ padding: '10px 14px', color: 'var(--accent)' }}>Null</td>
                  <td style={{ padding: '10px 14px' }}><code>nothing</code> (or <code>null</code>)</td>
                  <td style={{ padding: '10px 14px' }}>Represents absence of a value. Falsey.</td>
                </tr>
                <tr style={{ borderBottom: '1px solid var(--border-subtle)' }}>
                  <td style={{ padding: '10px 14px', color: 'var(--accent)' }}>List</td>
                  <td style={{ padding: '10px 14px' }}><code>[1, 2, "three"]</code></td>
                  <td style={{ padding: '10px 14px' }}>0-based mutable indexed list.</td>
                </tr>
                <tr style={{ borderBottom: '1px solid var(--border-subtle)' }}>
                  <td style={{ padding: '10px 14px', color: 'var(--accent)' }}>Dictionary</td>
                  <td style={{ padding: '10px 14px' }}><code>{`{ name: "Alice", age: 30 }`}</code></td>
                  <td style={{ padding: '10px 14px' }}>Key-value store preserving distinct types.</td>
                </tr>
                <tr>
                  <td style={{ padding: '10px 14px', color: 'var(--accent)' }}>Function</td>
                  <td style={{ padding: '10px 14px' }}><code>{`<function greet>`}</code></td>
                  <td style={{ padding: '10px 14px' }}>First-class callable closures.</td>
                </tr>
              </tbody>
            </table>
          </div>

          <h2 style={{ fontSize: '1.5rem', marginTop: '36px', marginBottom: '16px' }}>3. English Comparison Phrases</h2>
          <p style={{ marginBottom: '14px' }}>
            Clarity offers natural English aliases identical in precedence and behavior to symbolic operators:
          </p>
          <CodeBlock
            code={`set age to 18

if age is at least 18 {
    say "Eligible for adult account"
}

if score is greater than 90 {
    say "Honor roll achieved"
}`}
            filename="comparisons.clr"
          />

          <h2 style={{ fontSize: '1.5rem', marginTop: '36px', marginBottom: '16px' }}>4. Functions & Closures</h2>
          <p style={{ marginBottom: '14px' }}>
            Functions are declared with <code>function</code> and parameters are declared using <code>taking ... and ...</code>:
          </p>
          <CodeBlock
            code={`function make_multiplier taking factor {
    function multiply taking number {
        return number * factor
    }
    return multiply
}

set triple to make_multiplier(3)
say triple(10)  # 30`}
            filename="closures.clr"
            output="30"
          />

          <h2 style={{ fontSize: '1.5rem', marginTop: '36px', marginBottom: '16px' }}>5. Collections & Indexing</h2>
          <CodeBlock
            code={`set items to ["Sword", "Shield"]
push "Potion" to items
set items[0] to "Magic Sword"

say items[0]  # "Magic Sword"

set player to { name: "Creebrine", hp: 100 }
say player["name"]
set player["hp"] to 90`}
            filename="data.clr"
          />
        </div>
      ),
    },
    {
      id: 'standard-library',
      title: 'Standard Library',
      description: 'Standard library reference for text manipulation, math utilities, collections, and file operations.',
      icon: <BookOpen size={17} />,
      content: (
        <div>
          <div style={{ marginBottom: '28px' }}>
            <span className="badge" style={{ marginBottom: '8px' }}>Built-in Library</span>
            <h1 style={{ fontSize: '2.4rem', marginBottom: '12px' }}>Standard Library Reference</h1>
            <p style={{ fontSize: '1.1rem', color: 'var(--text-secondary)' }}>
              Core standard library functions globally available in Clarity 0.5.0 as first-class values.
            </p>
          </div>

          <h2 style={{ fontSize: '1.4rem', color: 'var(--accent)', marginTop: '28px', marginBottom: '14px' }}>
            Text Functions
          </h2>
          <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '12px', marginBottom: '24px' }}>
            <li className="card" style={{ padding: '16px 20px' }}>
              <code>length(text)</code> — Returns number of Unicode characters in string.
            </li>
            <li className="card" style={{ padding: '16px 20px' }}>
              <code>uppercase(text)</code> — Converts string to uppercase.
            </li>
            <li className="card" style={{ padding: '16px 20px' }}>
              <code>lowercase(text)</code> — Converts string to lowercase.
            </li>
            <li className="card" style={{ padding: '16px 20px' }}>
              <code>trim(text)</code> — Strips leading and trailing whitespace.
            </li>
            <li className="card" style={{ padding: '16px 20px' }}>
              <code>contains(text, substring)</code> — Checks substring presence.
            </li>
            <li className="card" style={{ padding: '16px 20px' }}>
              <code>replace(text, old, new)</code> — Replaces all occurrences.
            </li>
            <li className="card" style={{ padding: '16px 20px' }}>
              <code>split(text, separator)</code> — Splits into list of strings.
            </li>
            <li className="card" style={{ padding: '16px 20px' }}>
              <code>join(items, separator)</code> — Joins list elements into string.
            </li>
          </ul>

          <h2 style={{ fontSize: '1.4rem', color: 'var(--accent)', marginTop: '36px', marginBottom: '14px' }}>
            Collection Functions
          </h2>
          <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '12px', marginBottom: '24px' }}>
            <li className="card" style={{ padding: '16px 20px' }}>
              <code>reverse(collection)</code> — Non-mutating; returns new reversed list or string.
            </li>
            <li className="card" style={{ padding: '16px 20px' }}>
              <code>sort(collection)</code> — Non-mutating; returns sorted list (all numbers or all strings).
            </li>
            <li className="card" style={{ padding: '16px 20px' }}>
              <code>contains(collection, value)</code> — Checks element in list or key in dictionary.
            </li>
            <li className="card" style={{ padding: '16px 20px' }}>
              <code>length(collection)</code> — Returns item count in list or dictionary.
            </li>
          </ul>

          <h2 style={{ fontSize: '1.4rem', color: 'var(--accent)', marginTop: '36px', marginBottom: '14px' }}>
            Math Functions
          </h2>
          <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '12px', marginBottom: '24px' }}>
            <li className="card" style={{ padding: '16px 20px' }}>
              <code>abs(number)</code> — Absolute value of number.
            </li>
            <li className="card" style={{ padding: '16px 20px' }}>
              <code>floor(number)</code> / <code>ceil(number)</code> — Integer floor / ceiling.
            </li>
            <li className="card" style={{ padding: '16px 20px' }}>
              <code>round(number [, digits])</code> — Rounds to integer or decimal digits.
            </li>
            <li className="card" style={{ padding: '16px 20px' }}>
              <code>min(...)</code> / <code>max(...)</code> — Minimum / maximum among arguments or list.
            </li>
            <li className="card" style={{ padding: '16px 20px' }}>
              <code>sqrt(number)</code> — Square root (exact integer if perfect square).
            </li>
            <li className="card" style={{ padding: '16px 20px' }}>
              <code>power(base, exponent)</code> — Exponentiation (<code>base ** exponent</code>).
            </li>
          </ul>

          <h2 style={{ fontSize: '1.4rem', color: 'var(--accent)', marginTop: '36px', marginBottom: '14px' }}>
            Random & File Operations
          </h2>
          <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '12px', marginBottom: '24px' }}>
            <li className="card" style={{ padding: '16px 20px' }}>
              <code>random(min, max)</code> — Inclusive integer random if integer bounds; float otherwise.
            </li>
            <li className="card" style={{ padding: '16px 20px' }}>
              <code>choose(items)</code> — Random choice from non-empty list or string.
            </li>
            <li className="card" style={{ padding: '16px 20px' }}>
              <code>read_file(path)</code> — Reads UTF-8 file (raises Clarity runtime error if missing).
            </li>
            <li className="card" style={{ padding: '16px 20px' }}>
              <code>write_file(path, content)</code> — Writes UTF-8 file (creates parent directories).
            </li>
            <li className="card" style={{ padding: '16px 20px' }}>
              <code>file_exists(path)</code> — Returns <code>true</code> / <code>false</code>.
            </li>
          </ul>
        </div>
      ),
    },
    {
      id: 'examples',
      title: 'Examples Walkthrough',
      description: 'Curated scripts and runnable examples demonstrating Clarity language features and patterns.',
      icon: <Sparkles size={17} />,
      content: (
        <div>
          <div style={{ marginBottom: '28px' }}>
            <span className="badge" style={{ marginBottom: '8px' }}>Practical Code</span>
            <h1 style={{ fontSize: '2.4rem', marginBottom: '12px' }}>Examples Walkthrough</h1>
            <p style={{ fontSize: '1.1rem', color: 'var(--text-secondary)' }}>
              Curated scripts from the repository demonstrating language features in action.
            </p>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
            <div>
              <h3 style={{ fontSize: '1.2rem', marginBottom: '8px', color: 'var(--text-primary)' }}>
                1. Standard Library Showcase (`standard_library.clr`)
              </h3>
              <CodeBlock
                code={`set greeting to "  Welcome to Clarity  "
say "Trimmed & Uppercase: " + uppercase(trim(greeting))

set scores to [88, 42, 95, 70, 100]
say "Sorted scores: " + sort(scores)
say "Lowest score: " + min(scores)
say "Highest score: " + max(scores)
say "Square root of 81: " + sqrt(81)

set roll to random(1, 6)
say "Rolled a die (1-6): " + roll`}
                filename="standard_library.clr"
                output={`Trimmed & Uppercase: WELCOME TO CLARITY\nSorted scores: [42, 70, 88, 95, 100]\nLowest score: 42\nHighest score: 100\nSquare root of 81: 9\nRolled a die (1-6): 4`}
              />
            </div>

            <div>
              <h3 style={{ fontSize: '1.2rem', marginBottom: '8px', color: 'var(--text-primary)' }}>
                2. Data Access & English Comparisons (`data_access.clr`)
              </h3>
              <CodeBlock
                code={`set user to {
    name: "Creebrine",
    age: 14,
    scores: [95, 100]
}

if user["scores"][0] is at least 90 {
    say user["name"] + " passed with distinction!"
}

repeat 2 times {
    say "Great work!"
}`}
                filename="data_access.clr"
                output={`Creebrine passed with distinction!\nGreat work!\nGreat work!`}
              />
            </div>
          </div>
        </div>
      ),
    },
    {
      id: 'ecosystem',
      title: 'Ecosystem Architecture',
      description: 'Component boundaries, responsibilities, and architectural separation across the Clarity ecosystem.',
      icon: <Layers size={17} />,
      content: (
        <div>
          <div style={{ marginBottom: '28px' }}>
            <span className="badge" style={{ marginBottom: '8px' }}>Platform Map</span>
            <h1 style={{ fontSize: '2.4rem', marginBottom: '12px' }}>The Clarity Ecosystem</h1>
            <p style={{ fontSize: '1.1rem', color: 'var(--text-secondary)' }}>
              Component boundaries, responsibilities, and architectural separation of concerns.
            </p>
          </div>

          <h2 style={{ fontSize: '1.4rem', marginTop: '24px', marginBottom: '14px' }}>Decoupled Architecture</h2>
          <p style={{ marginBottom: '20px', lineHeight: 1.6 }}>
            Clarity is engineered around strict component decoupling. The language core is completely headless and free of UI, GUI, or platform-specific packaging dependencies.
          </p>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px', marginTop: '24px' }}>
            <div className="card">
              <h4 style={{ color: 'var(--accent)', marginBottom: '8px' }}>1. Language Core</h4>
              <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                Lexer, parser, AST, visitor evaluator, lexical closures, and built-in standard library.
              </p>
            </div>
            <div className="card">
              <h4 style={{ color: 'var(--accent-purple)', marginBottom: '8px' }}>2. Toolchain</h4>
              <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                CLI runner, project generator (`clarity new`), test harness (`clarity test`), and native OS installers.
              </p>
            </div>
            <div className="card">
              <h4 style={{ color: 'var(--accent-emerald)', marginBottom: '8px' }}>3. Website</h4>
              <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                Documentation, examples, downloads, and roadmap transparency at clarity.creebrine.com.
              </p>
            </div>
            <div className="card">
              <h4 style={{ color: 'var(--accent-rose)', marginBottom: '8px' }}>4. Clarity Editor</h4>
              <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                Dedicated development environment with real-time syntax diagnostics and autocomplete.
              </p>
            </div>
          </div>
        </div>
      ),
    },
    {
      id: 'spec',
      title: 'Formal Specification',
      description: 'Formal language specification for Clarity 0.5.0 including grammar rules, precedence, and error contracts.',
      icon: <FileText size={17} />,
      content: (
        <div>
          <div style={{ marginBottom: '28px' }}>
            <span className="badge" style={{ marginBottom: '8px' }}>Technical Contract</span>
            <h1 style={{ fontSize: '2.4rem', marginBottom: '12px' }}>Clarity 0.5.0 Specification</h1>
            <p style={{ fontSize: '1.1rem', color: 'var(--text-secondary)' }}>
              Summary of technical specifications, grammar rules, operator precedence, and error contracts.
            </p>
          </div>

          <div className="card" style={{ marginBottom: '24px' }}>
            <h3 style={{ fontSize: '1.15rem', marginBottom: '10px' }}>Operator Precedence (Low to High)</h3>
            <ol style={{ paddingLeft: '20px', fontSize: '0.92rem', color: 'var(--text-secondary)', display: 'flex', flexDirection: 'column', gap: '6px' }}>
              <li><code>or</code></li>
              <li><code>and</code></li>
              <li>Equality: <code>==</code>, <code>!=</code>, <code>is equal to</code>, <code>is not equal to</code></li>
              <li>Comparison: <code>&gt;</code>, <code>&lt;</code>, <code>&gt;=</code>, <code>&lt;=</code>, <code>is greater than</code>, <code>is at least</code>, etc.</li>
              <li>Additive: <code>+</code> (numeric add or string concat), <code>-</code></li>
              <li>Multiplicative: <code>*</code>, <code>/</code>, <code>%</code></li>
              <li>Unary: <code>not</code>, <code>-</code>, <code>+</code></li>
              <li>Postfix: function call <code>(...)</code>, indexing <code>[...]</code></li>
            </ol>
          </div>

          <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem' }}>
            The full authoritative specification is maintained in the repository at{' '}
            <a
              href="https://github.com/creebrinemc/clarity/blob/main/SPEC.md"
              target="_blank"
              rel="noopener noreferrer"
              style={{ color: 'var(--accent)' }}
            >
              SPEC.md on GitHub
            </a>.
          </p>
        </div>
      ),
    },
  ];

  const currentSection = sections.find((s) => s.id === activeTab) || sections[0];
  const currentIndex = sections.findIndex((s) => s.id === activeTab);
  const prevSection = currentIndex > 0 ? sections[currentIndex - 1] : null;
  const nextSection = currentIndex < sections.length - 1 ? sections[currentIndex + 1] : null;

  return (
    <div className="container" style={{ padding: '40px 24px 80px' }}>
      <SEO
        title={`${currentSection.title} — Clarity Documentation`}
        description={currentSection.description}
        canonicalPath={activeTab === 'getting-started' ? '/docs' : `/docs/${activeTab}`}
      />
      {/* Breadcrumb */}
      <nav
        aria-label="Breadcrumb"
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          fontSize: '0.85rem',
          color: 'var(--text-muted)',
          marginBottom: '28px',
        }}
      >
        <Link to="/" style={{ color: 'var(--text-muted)' }}>Home</Link>
        <ChevronRight size={14} aria-hidden="true" />
        <Link to="/docs" style={{ color: 'var(--text-muted)' }}>Docs</Link>
        <ChevronRight size={14} aria-hidden="true" />
        <span style={{ color: 'var(--text-primary)' }} aria-current="page">{currentSection.title}</span>
      </nav>

      <div
        style={{
          display: 'grid',
          gridTemplateColumns: '260px 1fr',
          gap: '48px',
          alignItems: 'start',
        }}
        className="docs-layout"
      >
        {/* Desktop Sidebar */}
        <aside
          aria-label="Documentation navigation"
          style={{
            position: 'sticky',
            top: '90px',
            display: 'flex',
            flexDirection: 'column',
            gap: '6px',
            background: 'var(--bg-surface)',
            padding: '16px',
            borderRadius: 'var(--radius-lg)',
            border: '1px solid var(--border-subtle)',
          }}
          className="docs-sidebar"
        >
          <div
            style={{
              fontSize: '0.78rem',
              textTransform: 'uppercase',
              letterSpacing: '0.06em',
              color: 'var(--text-muted)',
              padding: '6px 12px',
              fontWeight: 600,
            }}
          >
            Navigation
          </div>

          {sections.map((section) => {
            const active = section.id === activeTab;
            return (
              <Link
                key={section.id}
                to={`/docs/${section.id}`}
                aria-current={active ? 'page' : undefined}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '10px',
                  padding: '10px 12px',
                  borderRadius: 'var(--radius-md)',
                  textDecoration: 'none',
                  background: active ? 'rgba(56, 189, 248, 0.12)' : 'transparent',
                  color: active ? 'var(--accent)' : 'var(--text-secondary)',
                  fontWeight: active ? 600 : 500,
                  fontSize: '0.9rem',
                  cursor: 'pointer',
                  textAlign: 'left',
                  width: '100%',
                  transition: 'all 0.15s ease',
                }}
              >
                {section.icon}
                <span>{section.title}</span>
              </Link>
            );
          })}
        </aside>

        {/* Content Area */}
        <div style={{ minWidth: 0 }}>
          {currentSection.content}

          {/* Prev / Next Navigation Footer */}
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              borderTop: '1px solid var(--border-subtle)',
              paddingTop: '32px',
              marginTop: '48px',
              gap: '16px',
            }}
          >
            {prevSection ? (
              <Link
                to={`/docs/${prevSection.id}`}
                className="btn btn-secondary"
                style={{ fontSize: '0.88rem' }}
                aria-label={`Previous section: ${prevSection.title}`}
              >
                <ArrowLeft size={15} />
                <span>{prevSection.title}</span>
              </Link>
            ) : <div />}

            {nextSection && (
              <Link
                to={`/docs/${nextSection.id}`}
                className="btn btn-secondary"
                style={{ fontSize: '0.88rem' }}
                aria-label={`Next section: ${nextSection.title}`}
              >
                <span>{nextSection.title}</span>
                <ArrowRight size={15} />
              </Link>
            )}
          </div>
        </div>
      </div>

      <style>{`
        @media (max-width: 860px) {
          .docs-layout {
            grid-template-columns: 1fr !important;
            gap: 24px !important;
          }
          .docs-sidebar {
            position: static !important;
            display: grid !important;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)) !important;
          }
        }
      `}</style>
    </div>
  );
};
