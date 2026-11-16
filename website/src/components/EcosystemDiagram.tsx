import React, { useState } from 'react';
import { Cpu, Terminal, Globe, Code2, CheckCircle2, Clock, Sparkles } from 'lucide-react';

interface ComponentInfo {
  id: string;
  title: string;
  subtitle: string;
  icon: React.ReactNode;
  status: 'active' | 'in-progress' | 'planned';
  statusLabel: string;
  description: string;
  items: string[];
}

const COMPONENTS: ComponentInfo[] = [
  {
    id: 'language',
    title: 'Language Core',
    subtitle: 'Headless Interpreter & Semantics',
    icon: <Cpu size={22} color="#38bdf8" />,
    status: 'active',
    statusLabel: 'v0.6.0 Complete',
    description:
      'The pure language engine: hand-written lexer, recursive-descent parser, AST with source spans, runtime evaluator, lexical closures, modules and imports, and built-in standard library.',
    items: [
      'Lexer & Parser with source-span tracking',
      'Visitor evaluator & lexical environments',
      'First-class functions & mutable closures',
      'Modules, imports & dot member access',
      'Built-in Standard Library (Text, Math, Files)',
    ],
  },
  {
    id: 'toolchain',
    title: 'Toolchain',
    subtitle: 'Developer Workflow & CLI',
    icon: <Terminal size={22} color="#818cf8" />,
    status: 'in-progress',
    statusLabel: 'In Progress',
    description:
      'High-level CLI tools for building, scaffolding, formatting, and distributing Clarity programs across operating systems.',
    items: [
      'CLI runner (`clarity <file.clr>`, `clarity run`)',
      'Project scaffolding (`clarity new`)',
      'Native test runner (`clarity test`)',
      'Windows installer (macOS & Linux planned)',
    ],
  },
  {
    id: 'website',
    title: 'Website',
    subtitle: 'clarity.creebrine.com',
    icon: <Globe size={22} color="#34d399" />,
    status: 'in-progress',
    statusLabel: 'In Development',
    description:
      'The official web platform and documentation portal providing interactive guides, real-world examples, downloads, and roadmap transparency.',
    items: [
      'Getting Started & Language Guides',
      'Standard Library Reference',
      'Interactive Code Highlighting & Showcase',
      'Downloads Hub & Release Changelogs',
    ],
  },
  {
    id: 'editor',
    title: 'Clarity Editor',
    subtitle: 'Dedicated .clr Development IDE',
    icon: <Code2 size={22} color="#f472b6" />,
    status: 'planned',
    statusLabel: 'Planned Future Tool',
    description:
      'A dedicated, lightweight development environment tailored for Clarity, featuring real-time parse diagnostics, autocompletion, and integrated execution.',
    items: [
      'Clarity-specific syntax coloring & formatting',
      'Real-time syntax diagnostics & error spans',
      'Intelligent autocomplete for builtins',
      'Integrated runner & output console',
    ],
  },
];

export const EcosystemDiagram: React.FC = () => {
  const [selectedId, setSelectedId] = useState<string>('language');
  const selected = COMPONENTS.find((c) => c.id === selectedId) || COMPONENTS[0];

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        gap: '20px',
      }}
    >
      {/* Visual Architectural Map Hierarchy */}
      <div
        style={{
          background: 'rgba(14, 18, 26, 0.7)',
          border: '1px solid var(--border-subtle)',
          borderRadius: 'var(--radius-lg)',
          padding: '18px 20px',
          display: 'flex',
          flexDirection: 'column',
          gap: '12px',
        }}
        className="ecosystem-architecture-banner"
      >
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '8px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.78rem', color: 'var(--accent)', fontWeight: 700, letterSpacing: '0.05em' }}>
              ECOSYSTEM ARCHITECTURE
            </span>
            <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>•</span>
            <span style={{ fontSize: '0.84rem', color: 'var(--text-secondary)' }}>
              Headless Core Foundation with Decoupled Toolchains & Interfaces
            </span>
          </div>
        </div>

        {/* Tree Diagram Connection Bar */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(4, 1fr)',
            gap: '10px',
          }}
          className="ecosystem-tree-grid"
        >
          {[
            { id: 'language', name: '1. Language Core', desc: 'Lexer • Parser • AST • Evaluator', color: 'var(--accent)' },
            { id: 'toolchain', name: '2. Toolchain', desc: 'CLI • Runner • Installers', color: 'var(--accent-purple)' },
            { id: 'website', name: '3. Website', desc: 'Docs • Guides • Portal', color: 'var(--accent-emerald)' },
            { id: 'editor', name: '4. Clarity Editor', desc: 'IDE • Syntax Diagnostics', color: 'var(--accent-rose)' },
          ].map((node) => {
            const isSelected = node.id === selectedId;
            return (
              <button
                key={node.id}
                onClick={() => setSelectedId(node.id)}
                style={{
                  background: isSelected ? 'rgba(56, 189, 248, 0.1)' : 'rgba(255, 255, 255, 0.02)',
                  border: isSelected ? '1px solid var(--accent)' : '1px solid var(--border-subtle)',
                  borderRadius: 'var(--radius-sm)',
                  padding: '8px 12px',
                  textAlign: 'left',
                  cursor: 'pointer',
                  transition: 'all 0.15s ease',
                }}
              >
                <div style={{ fontSize: '0.84rem', fontWeight: 600, color: isSelected ? 'var(--accent)' : 'var(--text-primary)', marginBottom: '2px' }}>
                  {node.name}
                </div>
                <div style={{ fontSize: '0.73rem', color: 'var(--text-muted)' }}>
                  {node.desc}
                </div>
              </button>
            );
          })}
        </div>

        {/* Visual Architecture Schematic Pipeline */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '8px',
            paddingTop: '6px',
            borderTop: '1px dashed var(--border-subtle)',
            fontSize: '0.76rem',
            fontFamily: 'var(--font-mono)',
            color: 'var(--text-muted)',
            flexWrap: 'wrap',
          }}
        >
          <span style={{ color: 'var(--accent)', fontWeight: 600 }}>Language Core (Pure AST/Runtime)</span>
          <span>&rarr;</span>
          <span style={{ color: 'var(--accent-purple)' }}>Toolchain (CLI &amp; Native Installers)</span>
          <span>&rarr;</span>
          <span style={{ color: 'var(--accent-emerald)' }}>Website</span>
          <span>&amp;</span>
          <span style={{ color: 'var(--accent-rose)' }}>Clarity Editor</span>
        </div>
      </div>

      {/* Cards Grid */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
          gap: '16px',
        }}
      >
        {COMPONENTS.map((item) => {
          const isSelected = item.id === selectedId;
          return (
            <div
              key={item.id}
              onClick={() => setSelectedId(item.id)}
              className="card"
              style={{
                cursor: 'pointer',
                borderColor: isSelected ? 'var(--accent)' : 'var(--border-subtle)',
                background: isSelected ? 'var(--bg-card-hover)' : 'var(--bg-card)',
                boxShadow: isSelected
                  ? '0 0 20px rgba(56, 189, 248, 0.15), 0 8px 24px rgba(0, 0, 0, 0.4)'
                  : 'none',
                transform: isSelected ? 'translateY(-2px)' : 'none',
                padding: '22px',
              }}
            >
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  marginBottom: '14px',
                }}
              >
                <div
                  style={{
                    width: '40px',
                    height: '40px',
                    borderRadius: '8px',
                    background: 'rgba(255, 255, 255, 0.04)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    border: '1px solid var(--border-subtle)',
                  }}
                >
                  {item.icon}
                </div>
                <span
                  className={`badge ${
                    item.status === 'active'
                      ? 'badge-success'
                      : item.status === 'in-progress'
                      ? ''
                      : 'badge-warning'
                  }`}
                  style={{ fontSize: '0.72rem' }}
                >
                  {item.status === 'active' ? (
                    <CheckCircle2 size={12} />
                  ) : item.status === 'in-progress' ? (
                    <Sparkles size={12} />
                  ) : (
                    <Clock size={12} />
                  )}
                  {item.statusLabel}
                </span>
              </div>

              <h3
                style={{
                  fontSize: '1.1rem',
                  fontWeight: 600,
                  color: 'var(--text-primary)',
                  marginBottom: '4px',
                }}
              >
                {item.title}
              </h3>
              <div
                style={{
                  fontSize: '0.82rem',
                  color: 'var(--text-muted)',
                  fontFamily: 'var(--font-mono)',
                }}
              >
                {item.subtitle}
              </div>
            </div>
          );
        })}
      </div>

      {/* Detail Pane */}
      <div
        className="card card-highlight"
        style={{
          padding: '28px',
        }}
      >
        <div
          style={{
            display: 'flex',
            flexWrap: 'wrap',
            alignItems: 'center',
            justifyContent: 'space-between',
            gap: '12px',
            marginBottom: '16px',
            borderBottom: '1px solid var(--border-subtle)',
            paddingBottom: '16px',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            {selected.icon}
            <div>
              <h4 style={{ fontSize: '1.2rem', color: 'var(--text-primary)' }}>
                {selected.title}
              </h4>
              <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                {selected.subtitle}
              </span>
            </div>
          </div>
          <span
            className={`badge ${
              selected.status === 'active'
                ? 'badge-success'
                : selected.status === 'in-progress'
                ? ''
                : 'badge-warning'
            }`}
          >
            {selected.statusLabel}
          </span>
        </div>

        <p
          style={{
            fontSize: '0.98rem',
            color: 'var(--text-secondary)',
            marginBottom: '20px',
            lineHeight: 1.6,
          }}
        >
          {selected.description}
        </p>

        <h5
          style={{
            fontSize: '0.85rem',
            textTransform: 'uppercase',
            letterSpacing: '0.06em',
            color: 'var(--text-primary)',
            marginBottom: '12px',
          }}
        >
          Key Scope & Features
        </h5>
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
            gap: '10px',
          }}
        >
          {selected.items.map((feat, idx) => (
            <div
              key={idx}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '10px',
                fontSize: '0.9rem',
                color: 'var(--text-primary)',
                background: 'rgba(255, 255, 255, 0.02)',
                padding: '10px 14px',
                borderRadius: 'var(--radius-sm)',
                border: '1px solid var(--border-subtle)',
              }}
            >
              <div
                style={{
                  width: '6px',
                  height: '6px',
                  borderRadius: '50%',
                  background: 'var(--accent)',
                }}
              />
              <span>{feat}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
