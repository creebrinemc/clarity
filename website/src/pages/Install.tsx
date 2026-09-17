import React from 'react';
import { Clock, AlertCircle } from 'lucide-react';
import { CodeBlock } from '../components/CodeBlock';
import { SEO } from '../components/SEO';

export const Install: React.FC = () => {
  return (
    <div className="container" style={{ padding: '60px 24px 100px', maxWidth: '840px' }}>
      <SEO
        title="Install Clarity"
        description="Step-by-step instructions for installing Clarity 0.5.0 in your local development environment."
        canonicalPath="/install"
      />
      <div style={{ textAlign: 'center', marginBottom: '48px' }}>
        <span className="badge badge-success" style={{ marginBottom: '12px' }}>
          Installation Guide
        </span>
        <h1 style={{ fontSize: '2.8rem', marginBottom: '16px' }}>Install Clarity</h1>
        <p style={{ fontSize: '1.15rem', color: 'var(--text-secondary)' }}>
          Get Clarity 0.5.0 set up in your local environment.
        </p>
      </div>

      {/* Honest Status Notice */}
      <div
        className="card"
        style={{
          borderLeft: '4px solid var(--accent)',
          background: 'rgba(56, 189, 248, 0.04)',
          marginBottom: '40px',
          padding: '20px 24px',
        }}
      >
        <div style={{ display: 'flex', gap: '14px', alignItems: 'flex-start' }}>
          <AlertCircle size={20} color="#38bdf8" style={{ marginTop: '2px', flexShrink: 0 }} />
          <div>
            <h4 style={{ fontSize: '1rem', color: 'var(--text-primary)', marginBottom: '4px' }}>
              Current Distribution Notice
            </h4>
            <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
              Clarity 0.5.0 is currently distributed as an open-source development prototype. A zero-configuration standalone native installer (Windows <code>.exe</code>, macOS <code>.pkg</code>, and Linux packages) is actively planned in the roadmap.
            </p>
          </div>
        </div>
      </div>

      {/* Current Installation Method */}
      <div style={{ marginBottom: '48px' }}>
        <h2 style={{ fontSize: '1.6rem', marginBottom: '8px' }}>
          1. Development Setup (Current)
        </h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '20px' }}>
          Requires <strong>Python 3.11 or newer</strong> and <strong>pip</strong>.
        </p>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <div>
            <h4 style={{ fontSize: '0.95rem', color: 'var(--text-primary)', marginBottom: '8px' }}>
              Step 1: Clone the Repository
            </h4>
            <CodeBlock
              code={`git clone https://github.com/creebrinemc/clarity.git
cd clarity`}
              filename="terminal"
              showLineNumbers={false}
            />
          </div>

          <div>
            <h4 style={{ fontSize: '0.95rem', color: 'var(--text-primary)', marginBottom: '8px' }}>
              Step 2: Create a Virtual Environment & Install
            </h4>
            <CodeBlock
              code={`# Create virtual environment
python3 -m venv .venv

# Activate environment
# On macOS / Linux:
source .venv/bin/activate

# On Windows:
.venv\\Scripts\\activate

# Install Clarity in editable mode
pip install -e ".[dev]"`}
              filename="terminal"
              showLineNumbers={false}
            />
          </div>

          <div>
            <h4 style={{ fontSize: '0.95rem', color: 'var(--text-primary)', marginBottom: '8px' }}>
              Step 3: Verify Installation
            </h4>
            <CodeBlock
              code={`clarity --version
# Output: Clarity 0.5.0`}
              filename="terminal"
              showLineNumbers={false}
            />
          </div>
        </div>
      </div>

      {/* Running Your First Script */}
      <div style={{ marginBottom: '56px' }}>
        <h2 style={{ fontSize: '1.6rem', marginBottom: '8px' }}>
          2. Running Scripts
        </h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '16px' }}>
          Pass any <code>.clr</code> source file directly to the <code>clarity</code> command:
        </p>
        <CodeBlock
          code={`clarity examples/hello.clr
clarity examples/standard_library.clr`}
          filename="terminal"
          showLineNumbers={false}
        />
      </div>

      {/* Future Native Installers Preview */}
      <div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
          <Clock size={18} color="#f59e0b" />
          <h2 style={{ fontSize: '1.6rem' }}>
            Upcoming Native Installers (Planned)
          </h2>
        </div>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '24px' }}>
          Future releases will provide single-click installers that bundle the standalone runtime, eliminating the need for manual Python environment setup.
        </p>

        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
            gap: '16px',
          }}
        >
          <div className="card" style={{ padding: '20px' }}>
            <h4 style={{ color: 'var(--text-primary)', marginBottom: '6px' }}>Windows Setup</h4>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '12px' }}>
              Standalone <code>.exe</code> installer with automatic PATH setup and <code>.clr</code> file association.
            </p>
            <span className="badge badge-warning" style={{ fontSize: '0.72rem' }}>Coming Soon</span>
          </div>

          <div className="card" style={{ padding: '20px' }}>
            <h4 style={{ color: 'var(--text-primary)', marginBottom: '6px' }}>macOS Package</h4>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '12px' }}>
              Signed <code>.pkg</code> installer and official Homebrew tap (<code>brew install clarity</code>).
            </p>
            <span className="badge badge-warning" style={{ fontSize: '0.72rem' }}>Coming Soon</span>
          </div>

          <div className="card" style={{ padding: '20px' }}>
            <h4 style={{ color: 'var(--text-primary)', marginBottom: '6px' }}>Linux Packages</h4>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '12px' }}>
              Native <code>.deb</code> / <code>.rpm</code> binaries and a one-line curl install script.
            </p>
            <span className="badge badge-warning" style={{ fontSize: '0.72rem' }}>Coming Soon</span>
          </div>
        </div>
      </div>
    </div>
  );
};
