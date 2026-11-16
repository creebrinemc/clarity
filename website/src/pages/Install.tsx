import React from 'react';
import { Clock, AlertCircle } from 'lucide-react';
import { CodeBlock } from '../components/CodeBlock';
import { SEO } from '../components/SEO';

export const Install: React.FC = () => {
  return (
    <div className="container" style={{ padding: '50px 24px 80px', maxWidth: '840px' }}>
      <SEO
        title="Install Clarity"
        description="Install Clarity 0.6.0 with the Windows installer or from source on macOS, Linux, and Windows."
        canonicalPath="/install"
      />
      <div style={{ textAlign: 'center', marginBottom: '40px' }}>
        <span className="badge badge-success" style={{ marginBottom: '12px' }}>
          Installation Guide
        </span>
        <h1 className="page-title">Install Clarity</h1>
        <p style={{ fontSize: '1.15rem', color: 'var(--text-secondary)' }}>
          Get Clarity 0.6.0 set up in your local environment.
        </p>
      </div>

      {/* Status Notice */}
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
              Current Installation
            </h4>
            <p style={{ fontSize: '0.92rem', color: 'var(--text-secondary)', lineHeight: 1.55 }}>
              Clarity 0.6.0 is available as a native Windows installer (no Python required) and from source on every platform. Native macOS and Linux packages are planned for future releases.
            </p>
          </div>
        </div>
      </div>

      {/* Windows Installer */}
      <div style={{ marginBottom: '48px' }}>
        <h2 style={{ fontSize: '1.5rem', marginBottom: '8px' }}>
          1. Windows Installer
        </h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '20px' }}>
          Download <code>Clarity-0.6.0-Windows-x64-Setup.exe</code> from{' '}
          <a href="https://github.com/creebrinemc/clarity/releases" target="_blank" rel="noopener noreferrer">
            GitHub Releases
          </a>
          . The installer bundles a standalone runtime, can add Clarity to your <code>PATH</code>, and registers{' '}
          <code>.clr</code> file associations. Open a new terminal afterwards and verify:
        </p>
        <CodeBlock
          code={`clarity --version
# Output: Clarity 0.6.0`}
          filename="terminal"
          showLineNumbers={false}
        />
      </div>

      {/* Source Installation Method */}
      <div style={{ marginBottom: '48px' }}>
        <h2 style={{ fontSize: '1.5rem', marginBottom: '8px' }}>
          2. Setup from Source (macOS, Linux, Windows)
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
# Output: Clarity 0.6.0`}
              filename="terminal"
              showLineNumbers={false}
            />
          </div>
        </div>
      </div>

      {/* Running Your First Script */}
      <div style={{ marginBottom: '56px' }}>
        <h2 style={{ fontSize: '1.6rem', marginBottom: '8px' }}>
          3. Running Scripts &amp; Projects
        </h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '16px' }}>
          Pass any <code>.clr</code> source file directly to the <code>clarity</code> command, or create a project:
        </p>
        <CodeBlock
          code={`clarity examples/hello.clr

clarity new my-app
cd my-app
clarity run
clarity test`}
          filename="terminal"
          showLineNumbers={false}
        />
      </div>

      {/* Future Native Installers Preview */}
      <div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
          <Clock size={18} color="#f59e0b" />
          <h2 style={{ fontSize: '1.6rem' }}>
            Native Distribution Status
          </h2>
        </div>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '24px' }}>
          Future releases will extend standalone distribution to macOS and Linux, eliminating the need for manual Python environment setup.
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
            <span className="badge badge-success" style={{ fontSize: '0.72rem' }}>Available in 0.6.0</span>
          </div>

          <div className="card" style={{ padding: '20px' }}>
            <h4 style={{ color: 'var(--text-primary)', marginBottom: '6px' }}>macOS Package</h4>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '12px' }}>
              Official Homebrew tap and standalone binaries.
            </p>
            <span className="badge badge-warning" style={{ fontSize: '0.72rem' }}>Coming Soon</span>
          </div>

          <div className="card" style={{ padding: '20px' }}>
            <h4 style={{ color: 'var(--text-primary)', marginBottom: '6px' }}>Linux Packages</h4>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '12px' }}>
              Native <code>.deb</code> packages and portable standalone builds.
            </p>
            <span className="badge badge-warning" style={{ fontSize: '0.72rem' }}>Coming Soon</span>
          </div>
        </div>
      </div>
    </div>
  );
};
