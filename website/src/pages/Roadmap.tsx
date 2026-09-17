import React from 'react';
import { CheckCircle2, Clock, Sparkles } from 'lucide-react';
import { SEO } from '../components/SEO';

interface Milestone {
  version: string;
  title: string;
  status: 'completed' | 'in-progress' | 'planned';
  description: string;
  highlights: string[];
}

const MILESTONES: Milestone[] = [
  {
    version: '0.1.0',
    title: 'Core Language Foundation',
    status: 'completed',
    description: 'Initial language prototype establishing variable bindings, numeric evaluation, operator precedence, and basic output.',
    highlights: [
      '`set ... to ...` variable assignments',
      'Arithmetic operators (+, -, *, /, %)',
      '`say` output statement',
      'Source-span tracking for error diagnostics',
    ],
  },
  {
    version: '0.1.1',
    title: 'Foundation Hardening',
    status: 'completed',
    description: 'Lexer hardening, comment handling, and diagnostic error improvements.',
    highlights: [
      'Line comment support with `#`',
      'Unary operators (`not`, `-`, `+`)',
      'Accurate column and line diagnostic coordinates',
    ],
  },
  {
    version: '0.2.0',
    title: 'Control Flow',
    status: 'completed',
    description: 'Branching logic, multi-iteration loops, and loop control statements.',
    highlights: [
      '`if / else if / else` conditional blocks',
      '`while` loop evaluation',
      'Numeric range loops (`for i from start to end [step]`)',
      '`break` and `continue` control flow signals',
    ],
  },
  {
    version: '0.3.0',
    title: 'Functions & Closures',
    status: 'completed',
    description: 'First-class callable functions, explicit return statements, and lexical closure captures.',
    highlights: [
      'Function declarations with named parameter chains (`taking a and b`)',
      'First-class functions (assignable, passable, returnable)',
      'Lexical closure scope chains',
      'Direct and mutual recursion',
    ],
  },
  {
    version: '0.4.0',
    title: 'Data & Readability',
    status: 'completed',
    description: 'Collection structures, 0-based indexing, natural English comparison aliases, and repeat loops.',
    highlights: [
      '0-based list and dictionary indexing (`items[0]`, `dict["key"]`)',
      'Indexed assignments on mutable collections',
      'English comparison phrases (`is at least`, `is greater than`, etc.)',
      '`for each` loops and `repeat N times` loops',
    ],
  },
  {
    version: '0.5.0',
    title: 'Standard Library',
    status: 'completed',
    description: 'Built-in standard library across Text, Collections, Math, Random, and Files with strict Clarity error isolation.',
    highlights: [
      'Text manipulation (`trim`, `uppercase`, `split`, `join`, `replace`)',
      'Non-mutating `sort` and `reverse` collection functions',
      'Mathematical functions (`abs`, `floor`, `ceil`, `round`, `min`, `max`, `sqrt`, `power`)',
      'Random generation and choice (`random`, `choose`)',
      'UTF-8 filesystem operations (`read_file`, `write_file`, `file_exists`)',
      'Zero Python exception leaks; pure Clarity runtime diagnostics',
    ],
  },
  {
    version: '0.6.x',
    title: 'Modules & Project System',
    status: 'in-progress',
    description: 'Module import system, namespaces, and structured multi-file project resolution.',
    highlights: [
      '`import` statements and module namespaces',
      'Project manifest configuration (`clarity.toml`)',
      'Multi-file compilation and resolution',
    ],
  },
  {
    version: 'Toolchain',
    title: 'Developer Tooling',
    status: 'planned',
    description: 'Official CLI enhancements for project scaffolding, testing, and formatting.',
    highlights: [
      '`clarity new` project generator',
      '`clarity test` native test runner',
      '`clarity fmt` canonical code formatter',
    ],
  },
  {
    version: 'Installers',
    title: 'Native OS Distribution',
    status: 'planned',
    description: 'Zero-configuration standalone setup packages bundling the runtime for all major operating systems.',
    highlights: [
      'Windows standalone `.exe` installer with PATH and `.clr` file association',
      'macOS `.pkg` installer and Homebrew formula',
      'Linux native packages and standalone installation script',
    ],
  },
  {
    version: 'Website',
    title: 'Web Platform Launch',
    status: 'in-progress',
    description: 'Official documentation and ecosystem portal at clarity.creebrine.com.',
    highlights: [
      'Interactive documentation and syntax showcase',
      'Downloads hub and version release notes',
      'Community resources and guides',
    ],
  },
  {
    version: 'Editor',
    title: 'Dedicated Clarity IDE',
    status: 'planned',
    description: 'Tailored development environment for writing, inspecting, and debugging Clarity code.',
    highlights: [
      'Custom syntax colorization and real-time parse diagnostics',
      'Intelligent autocomplete for builtins and user declarations',
      'Integrated runner and output terminal',
    ],
  },
];

export const Roadmap: React.FC = () => {
  return (
    <div className="container" style={{ padding: '60px 24px 100px', maxWidth: '860px' }}>
      <SEO
        title="Clarity Roadmap"
        description="Explore the past, present, and future development milestones for the Clarity programming language and ecosystem."
        canonicalPath="/roadmap"
      />
      <div style={{ textAlign: 'center', marginBottom: '56px' }}>
        <span className="badge" style={{ marginBottom: '12px' }}>
          Milestone Tracker
        </span>
        <h1 style={{ fontSize: '2.8rem', marginBottom: '16px' }}>Project Roadmap</h1>
        <p style={{ fontSize: '1.15rem', color: 'var(--text-secondary)' }}>
          Transparent overview of completed language milestones and planned ecosystem components.
        </p>
      </div>

      {/* Timeline List */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
        {MILESTONES.map((m) => {
          const isDone = m.status === 'completed';
          const isInProgress = m.status === 'in-progress';
          return (
            <div
              key={m.version}
              className="card"
              style={{
                borderLeft: `4px solid ${
                  isDone ? 'var(--accent-emerald)' : isInProgress ? 'var(--accent)' : 'var(--border-medium)'
                }`,
                padding: '24px 28px',
              }}
            >
              <div
                style={{
                  display: 'flex',
                  flexWrap: 'wrap',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  gap: '10px',
                  marginBottom: '12px',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <span
                    style={{
                      fontFamily: 'var(--font-mono)',
                      fontSize: '1rem',
                      fontWeight: 700,
                      color: isDone ? 'var(--accent-emerald)' : 'var(--text-primary)',
                    }}
                  >
                    {m.version}
                  </span>
                  <span style={{ color: 'var(--text-muted)' }}>—</span>
                  <h3 style={{ fontSize: '1.2rem', color: 'var(--text-primary)' }}>
                    {m.title}
                  </h3>
                </div>

                <span
                  className={`badge ${
                    isDone ? 'badge-success' : isInProgress ? '' : 'badge-warning'
                  }`}
                  style={{ fontSize: '0.72rem' }}
                >
                  {isDone ? (
                    <CheckCircle2 size={12} />
                  ) : isInProgress ? (
                    <Sparkles size={12} />
                  ) : (
                    <Clock size={12} />
                  )}
                  {isDone ? 'Completed' : isInProgress ? 'In Progress' : 'Planned'}
                </span>
              </div>

              <p style={{ fontSize: '0.95rem', color: 'var(--text-secondary)', marginBottom: '16px', lineHeight: 1.6 }}>
                {m.description}
              </p>

              <div
                style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
                  gap: '8px',
                }}
              >
                {m.highlights.map((h, i) => (
                  <div
                    key={i}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '8px',
                      fontSize: '0.85rem',
                      color: 'var(--text-muted)',
                    }}
                  >
                    <div
                      style={{
                        width: '4px',
                        height: '4px',
                        borderRadius: '50%',
                        background: isDone ? 'var(--accent-emerald)' : 'var(--accent)',
                      }}
                    />
                    <span>{h}</span>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
