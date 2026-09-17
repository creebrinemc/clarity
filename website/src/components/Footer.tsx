import React from 'react';
import { Link } from 'react-router-dom';
import { Terminal } from 'lucide-react';
import { GithubIcon } from './GithubIcon';

export const Footer: React.FC = () => {
  return (
    <footer
      style={{
        borderTop: '1px solid var(--border-subtle)',
        background: 'var(--bg-surface)',
        padding: '60px 0 36px',
        marginTop: 'auto',
      }}
    >
      <div className="container">
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
            gap: '40px',
            marginBottom: '48px',
          }}
        >
          {/* Brand Col */}
          <div style={{ maxWidth: '320px' }}>
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '10px',
                marginBottom: '14px',
              }}
            >
              <div
                style={{
                  width: '28px',
                  height: '28px',
                  borderRadius: '6px',
                  background: 'var(--accent-gradient)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                }}
              >
                <Terminal size={16} color="#080a0f" strokeWidth={2.5} />
              </div>
              <span
                style={{
                  fontFamily: 'var(--font-heading)',
                  fontSize: '1.2rem',
                  fontWeight: 700,
                  color: 'var(--text-primary)',
                }}
              >
                Clarity
              </span>
            </div>
            <p
              style={{
                fontSize: '0.9rem',
                color: 'var(--text-secondary)',
                lineHeight: 1.6,
                marginBottom: '16px',
              }}
            >
              Code that speaks for itself. A general-purpose programming language designed around readable, expressive syntax.
            </p>
            <div
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px',
                fontSize: '0.78rem',
                color: 'var(--text-muted)',
              }}
            >
              <span>Current version:</span>
              <span className="badge" style={{ fontSize: '0.7rem', padding: '1px 6px' }}>
                0.5.0
              </span>
            </div>
          </div>

          {/* Resources */}
          <div>
            <h4
              style={{
                fontSize: '0.9rem',
                textTransform: 'uppercase',
                letterSpacing: '0.06em',
                color: 'var(--text-primary)',
                marginBottom: '16px',
              }}
            >
              Documentation
            </h4>
            <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '10px' }}>
              <li>
                <Link to="/docs" style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                  Overview & Quickstart
                </Link>
              </li>
              <li>
                <Link to="/docs/language" style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                  Language Guide
                </Link>
              </li>
              <li>
                <Link to="/docs/standard-library" style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                  Standard Library
                </Link>
              </li>
              <li>
                <Link to="/docs/spec" style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                  Language Specification (SPEC.md)
                </Link>
              </li>
            </ul>
          </div>

          {/* Ecosystem */}
          <div>
            <h4
              style={{
                fontSize: '0.9rem',
                textTransform: 'uppercase',
                letterSpacing: '0.06em',
                color: 'var(--text-primary)',
                marginBottom: '16px',
              }}
            >
              Ecosystem
            </h4>
            <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '10px' }}>
              <li>
                <Link to="/examples" style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                  Examples Showcase
                </Link>
              </li>
              <li>
                <Link to="/install" style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                  Installation & Setup
                </Link>
              </li>
              <li>
                <Link to="/roadmap" style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                  Milestones & Roadmap
                </Link>
              </li>
              <li>
                <Link to="/docs/ecosystem" style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                  Ecosystem Architecture
                </Link>
              </li>
            </ul>
          </div>

          {/* Community */}
          <div>
            <h4
              style={{
                fontSize: '0.9rem',
                textTransform: 'uppercase',
                letterSpacing: '0.06em',
                color: 'var(--text-primary)',
                marginBottom: '16px',
              }}
            >
              Project
            </h4>
            <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '10px' }}>
              <li>
                <a
                  href="https://github.com/creebrinemc/clarity"
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{
                    fontSize: '0.9rem',
                    color: 'var(--text-secondary)',
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '6px',
                  }}
                >
                  <GithubIcon size={15} />
                  <span>GitHub Repository</span>
                </a>
              </li>
              <li>
                <a
                  href="https://github.com/creebrinemc/clarity/issues"
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}
                >
                  Issue Tracker
                </a>
              </li>
              <li>
                <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                  MIT Licensed Open Source
                </span>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div
          style={{
            borderTop: '1px solid var(--border-subtle)',
            paddingTop: '24px',
            display: 'flex',
            flexWrap: 'wrap',
            alignItems: 'center',
            justifyContent: 'space-between',
            gap: '12px',
            fontSize: '0.85rem',
            color: 'var(--text-muted)',
          }}
        >
          <div>
            Clarity is designed and developed by{' '}
            <span style={{ color: 'var(--text-secondary)', fontWeight: 500 }}>Creebrine</span>.
          </div>
          <div>
            clarity.creebrine.com — Code that speaks for itself.
          </div>
        </div>
      </div>
    </footer>
  );
};
