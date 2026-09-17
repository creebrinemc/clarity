import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import {
  ArrowRight,
  BookOpen,
  Download,
  CheckCircle2,
  Sparkles,
  Layers,
  Compass,
  Cpu,
  Terminal,
} from 'lucide-react';
import { GithubIcon } from '../components/GithubIcon';
import { CodeBlock } from '../components/CodeBlock';
import { EcosystemDiagram } from '../components/EcosystemDiagram';
import { SEO } from '../components/SEO';

const HERO_CODE = `# hello.clr
set user to {
    name: "Creebrine",
    score: 100
}

function greet taking person {
    say "Hello, " + person["name"] + "!"
}

if user["score"] is at least 100 {
    greet(user)
}`;

const SHOWCASE_TABS = [
  {
    id: 'hello',
    title: 'Hello & Variables',
    filename: 'variables.clr',
    code: `set name to "Creebrine"
set level to 42

say "Welcome back, " + name
say "Current level: " + level`,
    output: `Welcome back, Creebrine\nCurrent level: 42`,
    description: 'Natural variable assignments with the nearest-binding scoping rule.',
  },
  {
    id: 'functions',
    title: 'Functions & Closures',
    filename: 'closures.clr',
    code: `function make_adder taking base {
    function add taking num {
        return base + num
    }
    return add
}

set add_five to make_adder(5)
say add_five(10)
say add_five(20)`,
    output: `15\n25`,
    description: 'First-class functions with lexical closures and named parameter chains.',
  },
  {
    id: 'collections',
    title: 'Data & Indexing',
    filename: 'inventory.clr',
    code: `set hero to {
    name: "Creebrine",
    items: ["Sword", "Shield"]
}

push "Potion" to hero["items"]
set hero["items"][0] to "Master Sword"

say hero["name"] + " inventory:"
for each item in hero["items"] {
    say "- " + item
}`,
    output: `Creebrine inventory:\n- Master Sword\n- Shield\n- Potion`,
    description: '0-based indexing on lists, strings, and dictionary structures.',
  },
  {
    id: 'control_flow',
    title: 'Control Flow',
    filename: 'loops.clr',
    code: `set score to 95

if score is at least 90 {
    say "Grade: Excellent!"
}

repeat 3 times {
    say "Level up!"
}`,
    output: `Grade: Excellent!\nLevel up!\nLevel up!\nLevel up!`,
    description: 'Readable English comparison phrases and intuitive repeat loops.',
  },
  {
    id: 'stdlib',
    title: 'Standard Library',
    filename: 'stdlib.clr',
    code: `set raw_title to "  clarity language  "
say uppercase(trim(raw_title))

set scores to [88, 42, 95, 70]
say "Sorted: " + sort(scores)
say "Square root: " + sqrt(81)
say "Dice roll: " + random(1, 6)`,
    output: `CLARITY LANGUAGE\nSorted: [42, 70, 88, 95]\nSquare root: 9\nDice roll: 4`,
    description: 'Built-in functions for text, sorting, math, random, and files with strict error guarantees.',
  },
];

export const Home: React.FC = () => {
  const [activeTab, setActiveTab] = useState(SHOWCASE_TABS[0]);

  return (
    <div style={{ display: 'flex', flexDirection: 'column' }}>
      <SEO
        title="Clarity — Code that speaks for itself"
        description="Clarity is a general-purpose programming language designed around readable, expressive syntax without sacrificing structural certainty or future power."
        canonicalPath="/"
      />
      {/* ====================================================================
          HERO SECTION
          ==================================================================== */}
      <section
        style={{
          padding: '80px 0 60px',
          position: 'relative',
          overflow: 'hidden',
        }}
      >
        <div className="container">
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
              gap: '48px',
              alignItems: 'center',
            }}
          >
            {/* Hero Left Content */}
            <div style={{ maxWidth: '580px' }}>
              <div
                className="badge"
                style={{
                  marginBottom: '20px',
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '6px',
                }}
              >
                <Sparkles size={13} />
                <span>Clarity 0.5.0 Released</span>
              </div>

              <h1
                style={{
                  fontSize: 'clamp(2.5rem, 5vw, 3.8rem)',
                  fontWeight: 800,
                  lineHeight: 1.1,
                  marginBottom: '20px',
                  letterSpacing: '-0.03em',
                }}
              >
                Code that speaks{' '}
                <span
                  style={{
                    background: 'var(--accent-gradient)',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                  }}
                >
                  for itself.
                </span>
              </h1>

              <p
                style={{
                  fontSize: '1.18rem',
                  color: 'var(--text-secondary)',
                  lineHeight: 1.6,
                  marginBottom: '32px',
                }}
              >
                Clarity is a general-purpose programming language designed to make code easier to understand without sacrificing structure or future power.
              </p>

              <div
                style={{
                  display: 'flex',
                  flexWrap: 'wrap',
                  gap: '14px',
                  marginBottom: '36px',
                }}
              >
                <Link to="/install" className="btn btn-primary">
                  <Download size={17} />
                  <span>Get Clarity</span>
                  <ArrowRight size={15} />
                </Link>

                <Link to="/docs" className="btn btn-secondary">
                  <BookOpen size={17} />
                  <span>Read the Docs</span>
                </Link>

                <a
                  href="https://github.com/creebrinemc/clarity"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn btn-ghost"
                >
                  <GithubIcon size={17} />
                  <span>GitHub</span>
                </a>
              </div>

              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '24px',
                  paddingTop: '20px',
                  borderTop: '1px solid var(--border-subtle)',
                  fontSize: '0.85rem',
                  color: 'var(--text-muted)',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <CheckCircle2 size={15} color="#10b981" />
                  <span>199 Passing Tests</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <CheckCircle2 size={15} color="#10b981" />
                  <span>Zero Leaked Host Errors</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <CheckCircle2 size={15} color="#10b981" />
                  <span>MIT Open Source</span>
                </div>
              </div>
            </div>

            {/* Hero Right Code Visual */}
            <div>
              <CodeBlock
                code={HERO_CODE}
                filename="hello.clr"
                output="Hello, Creebrine!"
                showLineNumbers={true}
              />
            </div>
          </div>
        </div>
      </section>

      {/* ====================================================================
          "WHY CLARITY?" PILLARS SECTION
          ==================================================================== */}
      <section className="section" style={{ borderTop: '1px solid var(--border-subtle)' }}>
        <div className="container">
          <div style={{ textAlign: 'center', maxWidth: '640px', margin: '0 auto 56px' }}>
            <span className="badge" style={{ marginBottom: '12px' }}>
              Design Philosophy
            </span>
            <h2 style={{ fontSize: '2.2rem', marginBottom: '16px' }}>
              Why Clarity?
            </h2>
            <p style={{ fontSize: '1.05rem', color: 'var(--text-secondary)' }}>
              Clarity should read like structured English without becoming unnecessarily verbose.
            </p>
          </div>

          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
              gap: '20px',
            }}
          >
            <div className="card">
              <div
                style={{
                  width: '40px',
                  height: '40px',
                  borderRadius: '8px',
                  background: 'rgba(56, 189, 248, 0.1)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  marginBottom: '16px',
                  border: '1px solid rgba(56, 189, 248, 0.2)',
                }}
              >
                <Compass size={20} color="#38bdf8" />
              </div>
              <h3 style={{ fontSize: '1.2rem', marginBottom: '10px' }}>Readable</h3>
              <p style={{ fontSize: '0.92rem', color: 'var(--text-secondary)' }}>
                Syntax designed to be understandable at a glance. Programs read naturally for beginners and experienced developers alike.
              </p>
            </div>

            <div className="card">
              <div
                style={{
                  width: '40px',
                  height: '40px',
                  borderRadius: '8px',
                  background: 'rgba(129, 140, 248, 0.1)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  marginBottom: '16px',
                  border: '1px solid rgba(129, 140, 248, 0.2)',
                }}
              >
                <Layers size={20} color="#818cf8" />
              </div>
              <h3 style={{ fontSize: '1.2rem', marginBottom: '10px' }}>Structured</h3>
              <p style={{ fontSize: '0.92rem', color: 'var(--text-secondary)' }}>
                Natural-language-inspired syntax maintains rigorous computational certainty, strict scoping rules, and predictable semantics.
              </p>
            </div>

            <div className="card">
              <div
                style={{
                  width: '40px',
                  height: '40px',
                  borderRadius: '8px',
                  background: 'rgba(16, 185, 129, 0.1)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  marginBottom: '16px',
                  border: '1px solid rgba(16, 185, 129, 0.2)',
                }}
              >
                <Cpu size={20} color="#10b981" />
              </div>
              <h3 style={{ fontSize: '1.2rem', marginBottom: '10px' }}>General-Purpose</h3>
              <p style={{ fontSize: '0.92rem', color: 'var(--text-secondary)' }}>
                Intended to grow toward applications, developer tools, games, web backends, and system automation.
              </p>
            </div>

            <div className="card">
              <div
                style={{
                  width: '40px',
                  height: '40px',
                  borderRadius: '8px',
                  background: 'rgba(244, 114, 182, 0.1)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  marginBottom: '16px',
                  border: '1px solid rgba(244, 114, 182, 0.2)',
                }}
              >
                <Terminal size={20} color="#f472b6" />
              </div>
              <h3 style={{ fontSize: '1.2rem', marginBottom: '10px' }}>Built to Grow</h3>
              <p style={{ fontSize: '0.92rem', color: 'var(--text-secondary)' }}>
                The core language is the heart of an expanding ecosystem of toolchains, native installers, and dedicated editor tools.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* ====================================================================
          READABILITY IN ACTION (COMPARISON) SECTION
          ==================================================================== */}
      <section
        className="section"
        style={{
          background: 'var(--bg-surface)',
          borderTop: '1px solid var(--border-subtle)',
          borderBottom: '1px solid var(--border-subtle)',
        }}
      >
        <div className="container">
          <div style={{ textAlign: 'center', maxWidth: '640px', margin: '0 auto 48px' }}>
            <span className="badge" style={{ marginBottom: '12px' }}>
              Expressiveness
            </span>
            <h2 style={{ fontSize: '2.2rem', marginBottom: '16px' }}>
              Readability by Design
            </h2>
            <p style={{ fontSize: '1.05rem', color: 'var(--text-secondary)' }}>
              Clarity makes deliberate choices to favor clarity of thought over symbolic brevity.
            </p>
          </div>

          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
              gap: '24px',
            }}
          >
            {/* Card 1: Comparisons */}
            <div className="card">
              <h4 style={{ fontSize: '1.1rem', marginBottom: '12px', color: 'var(--text-primary)' }}>
                English Comparison Phrases
              </h4>
              <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '16px' }}>
                Comparisons can be written as natural English phrases or traditional symbols.
              </p>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                <div
                  style={{
                    background: 'var(--bg-code)',
                    padding: '10px 14px',
                    borderRadius: 'var(--radius-sm)',
                    fontFamily: 'var(--font-mono)',
                    fontSize: '0.88rem',
                    color: 'var(--accent)',
                    border: '1px solid var(--border-subtle)',
                  }}
                >
                  if score is at least 100 {'{ ... }'}
                </div>
                <div
                  style={{
                    background: 'rgba(255, 255, 255, 0.02)',
                    padding: '10px 14px',
                    borderRadius: 'var(--radius-sm)',
                    fontFamily: 'var(--font-mono)',
                    fontSize: '0.88rem',
                    color: 'var(--text-muted)',
                  }}
                >
                  if score is greater than threshold {'{ ... }'}
                </div>
              </div>
            </div>

            {/* Card 2: Named Parameter Chains */}
            <div className="card">
              <h4 style={{ fontSize: '1.1rem', marginBottom: '12px', color: 'var(--text-primary)' }}>
                Readable Function Declarations
              </h4>
              <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '16px' }}>
                Function parameters use clear parameter chains that describe input intent.
              </p>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                <div
                  style={{
                    background: 'var(--bg-code)',
                    padding: '10px 14px',
                    borderRadius: 'var(--radius-sm)',
                    fontFamily: 'var(--font-mono)',
                    fontSize: '0.88rem',
                    color: 'var(--accent)',
                    border: '1px solid var(--border-subtle)',
                  }}
                >
                  function add taking a and b {'{ return a + b }'}
                </div>
                <div
                  style={{
                    background: 'rgba(255, 255, 255, 0.02)',
                    padding: '10px 14px',
                    borderRadius: 'var(--radius-sm)',
                    fontFamily: 'var(--font-mono)',
                    fontSize: '0.88rem',
                    color: 'var(--text-muted)',
                  }}
                >
                  function greet taking person {'{ say "Hi, " + person }'}
                </div>
              </div>
            </div>

            {/* Card 3: Explicit Loops */}
            <div className="card">
              <h4 style={{ fontSize: '1.1rem', marginBottom: '12px', color: 'var(--text-primary)' }}>
                Intuitive Loop Forms
              </h4>
              <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '16px' }}>
                Express intent directly with `for each`, range loops, or `repeat N times`.
              </p>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                <div
                  style={{
                    background: 'var(--bg-code)',
                    padding: '10px 14px',
                    borderRadius: 'var(--radius-sm)',
                    fontFamily: 'var(--font-mono)',
                    fontSize: '0.88rem',
                    color: 'var(--accent)',
                    border: '1px solid var(--border-subtle)',
                  }}
                >
                  repeat 3 times {'{ say "Hooray!" }'}
                </div>
                <div
                  style={{
                    background: 'rgba(255, 255, 255, 0.02)',
                    padding: '10px 14px',
                    borderRadius: 'var(--radius-sm)',
                    fontFamily: 'var(--font-mono)',
                    fontSize: '0.88rem',
                    color: 'var(--text-muted)',
                  }}
                >
                  for each item in inventory {'{ say item }'}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ====================================================================
          INTERACTIVE LANGUAGE SHOWCASE
          ==================================================================== */}
      <section className="section">
        <div className="container">
          <div style={{ textAlign: 'center', maxWidth: '640px', margin: '0 auto 40px' }}>
            <span className="badge" style={{ marginBottom: '12px' }}>
              Hands-On
            </span>
            <h2 style={{ fontSize: '2.2rem', marginBottom: '16px' }}>
              Language Showcase
            </h2>
            <p style={{ fontSize: '1.05rem', color: 'var(--text-secondary)' }}>
              Explore how Clarity 0.5.0 handles everyday programming tasks.
            </p>
          </div>

          {/* Showcase Tabs */}
          <div
            style={{
              display: 'flex',
              flexWrap: 'wrap',
              gap: '8px',
              justifyContent: 'center',
              marginBottom: '28px',
            }}
          >
            {SHOWCASE_TABS.map((tab) => {
              const active = tab.id === activeTab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab)}
                  className={`btn ${active ? 'btn-primary' : 'btn-secondary'}`}
                  style={{
                    padding: '8px 18px',
                    fontSize: '0.88rem',
                  }}
                >
                  {tab.title}
                </button>
              );
            })}
          </div>

          <div style={{ maxWidth: '840px', margin: '0 auto' }}>
            <CodeBlock
              code={activeTab.code}
              filename={activeTab.filename}
              output={activeTab.output}
              showLineNumbers={true}
            />
            <p
              style={{
                fontSize: '0.9rem',
                color: 'var(--text-muted)',
                textAlign: 'center',
                marginTop: '16px',
              }}
            >
              {activeTab.description}
            </p>
          </div>
        </div>
      </section>

      {/* ====================================================================
          THE CLARITY ECOSYSTEM
          ==================================================================== */}
      <section
        className="section"
        style={{
          background: 'var(--bg-surface)',
          borderTop: '1px solid var(--border-subtle)',
          borderBottom: '1px solid var(--border-subtle)',
        }}
      >
        <div className="container">
          <div style={{ textAlign: 'center', maxWidth: '680px', margin: '0 auto 48px' }}>
            <span className="badge" style={{ marginBottom: '12px' }}>
              Platform Architecture
            </span>
            <h2 style={{ fontSize: '2.2rem', marginBottom: '16px' }}>
              The Clarity Ecosystem
            </h2>
            <p style={{ fontSize: '1.05rem', color: 'var(--text-secondary)' }}>
              Clarity is built on strict decoupling: the language core is headless and pure, surrounded by dedicated toolchains, portals, and editor tools.
            </p>
          </div>

          <EcosystemDiagram />
        </div>
      </section>

      {/* ====================================================================
          CURRENT STATUS & ROADMAP
          ==================================================================== */}
      <section className="section">
        <div className="container">
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
              gap: '40px',
              alignItems: 'start',
            }}
          >
            <div>
              <span className="badge badge-success" style={{ marginBottom: '12px' }}>
                Completed Milestones
              </span>
              <h2 style={{ fontSize: '2rem', marginBottom: '16px' }}>
                Active Progress
              </h2>
              <p style={{ color: 'var(--text-secondary)', marginBottom: '24px' }}>
                Clarity 0.5.0 is the result of continuous, test-driven language design passes.
              </p>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                {[
                  { ver: '0.1.0', name: 'Core Language', desc: 'Variables, math operators, precedence, say output.' },
                  { ver: '0.1.1', name: 'Foundation Hardening', desc: 'Lexer improvements, comments, unary operators, source spans.' },
                  { ver: '0.2.0', name: 'Control Flow', desc: 'if/else if/else, while, numeric range loops, break/continue.' },
                  { ver: '0.3.0', name: 'Functions & Closures', desc: 'First-class functions, parameter chains, return, lexical closures.' },
                  { ver: '0.4.0', name: 'Data & Readability', desc: 'List/dict/string indexing, for each, repeat N times, comparison phrases.' },
                  { ver: '0.5.0', name: 'Standard Library', desc: 'Built-in Text, Collections, Math, Random, and Files with zero Python exception leaks.' },
                ].map((item) => (
                  <div
                    key={item.ver}
                    style={{
                      display: 'flex',
                      alignItems: 'flex-start',
                      gap: '12px',
                      padding: '12px 16px',
                      background: 'var(--bg-card)',
                      borderRadius: 'var(--radius-md)',
                      border: '1px solid var(--border-subtle)',
                    }}
                  >
                    <CheckCircle2 size={18} color="#10b981" style={{ marginTop: '2px', flexShrink: 0 }} />
                    <div>
                      <div style={{ fontWeight: 600, fontSize: '0.95rem', color: 'var(--text-primary)' }}>
                        {item.ver} — {item.name}
                      </div>
                      <div style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>
                        {item.desc}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <span className="badge" style={{ marginBottom: '12px' }}>
                Upcoming Milestones
              </span>
              <h2 style={{ fontSize: '2rem', marginBottom: '16px' }}>
                Future Direction
              </h2>
              <p style={{ color: 'var(--text-secondary)', marginBottom: '24px' }}>
                Upcoming enhancements planned for the Clarity language and ecosystem.
              </p>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                {[
                  { name: '0.6.x — Modules & Projects', desc: 'File imports, namespaces, and structured multi-file project resolution.' },
                  { name: 'Toolchain Enhancements', desc: 'Project scaffolding (`clarity new`), test harness (`clarity test`), and code formatter.' },
                  { name: 'Native Standalone Installers', desc: 'Zero-config installers for Windows (.exe), macOS (.pkg/brew), and Linux.' },
                  { name: 'Clarity Website Launch', desc: 'Interactive web platform and documentation portal at clarity.creebrine.com.' },
                  { name: 'Dedicated Clarity Editor', desc: 'Lightweight development environment with real-time parse diagnostics and auto-completion.' },
                ].map((item, idx) => (
                  <div
                    key={idx}
                    style={{
                      display: 'flex',
                      alignItems: 'flex-start',
                      gap: '12px',
                      padding: '12px 16px',
                      background: 'rgba(255, 255, 255, 0.02)',
                      borderRadius: 'var(--radius-md)',
                      border: '1px solid var(--border-subtle)',
                    }}
                  >
                    <div
                      style={{
                        width: '18px',
                        height: '18px',
                        borderRadius: '50%',
                        border: '2px dashed var(--accent)',
                        marginTop: '2px',
                        flexShrink: 0,
                      }}
                    />
                    <div>
                      <div style={{ fontWeight: 600, fontSize: '0.95rem', color: 'var(--text-primary)' }}>
                        {item.name}
                      </div>
                      <div style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>
                        {item.desc}
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              <div style={{ marginTop: '24px' }}>
                <Link to="/roadmap" className="btn btn-secondary" style={{ width: '100%', justifyContent: 'center' }}>
                  <span>View Full Roadmap</span>
                  <ArrowRight size={15} />
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ====================================================================
          CALL TO ACTION (OPEN SOURCE & GITHUB)
          ==================================================================== */}
      <section
        className="section"
        style={{
          borderTop: '1px solid var(--border-subtle)',
          background: 'linear-gradient(180deg, var(--bg-surface) 0%, var(--bg-body) 100%)',
          textAlign: 'center',
        }}
      >
        <div className="container" style={{ maxWidth: '680px' }}>
          <h2 style={{ fontSize: '2.4rem', marginBottom: '16px' }}>
            Join the Clarity Journey
          </h2>
          <p
            style={{
              fontSize: '1.1rem',
              color: 'var(--text-secondary)',
              lineHeight: 1.6,
              marginBottom: '32px',
            }}
          >
            Clarity is completely open source under the MIT License. Explore the implementation, inspect tests, and follow milestone progress.
          </p>
          <div style={{ display: 'flex', justifyContent: 'center', gap: '16px', flexWrap: 'wrap' }}>
            <a
              href="https://github.com/creebrinemc/clarity"
              target="_blank"
              rel="noopener noreferrer"
              className="btn btn-primary"
            >
              <GithubIcon size={18} />
              <span>Explore on GitHub</span>
            </a>
            <Link to="/docs" className="btn btn-secondary">
              <BookOpen size={18} />
              <span>Read Documentation</span>
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};
