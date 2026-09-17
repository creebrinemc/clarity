import React from 'react';
import { Link } from 'react-router-dom';
import { Terminal, ArrowLeft } from 'lucide-react';
import { SEO } from '../components/SEO';

export const NotFound: React.FC = () => {
  return (
    <div
      className="container"
      style={{
        padding: '120px 24px',
        textAlign: 'center',
        maxWidth: '560px',
        margin: '0 auto',
      }}
    >
      <SEO
        title="404 — Page Not Found"
        description="The requested page could not be found on the Clarity website."
      />
      <div
        style={{
          width: '64px',
          height: '64px',
          borderRadius: '16px',
          background: 'rgba(56, 189, 248, 0.08)',
          border: '1px solid rgba(56, 189, 248, 0.2)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          margin: '0 auto 24px',
        }}
      >
        <Terminal size={32} color="#38bdf8" />
      </div>

      <span
        style={{
          fontFamily: 'var(--font-mono)',
          fontSize: '1rem',
          color: 'var(--accent)',
          fontWeight: 700,
        }}
      >
        404 — Not Found
      </span>

      <h1
        style={{
          fontSize: '2.4rem',
          margin: '12px 0 16px',
        }}
      >
        This page doesn't exist.
      </h1>

      <p
        style={{
          fontSize: '1.1rem',
          color: 'var(--text-secondary)',
          lineHeight: 1.6,
          marginBottom: '32px',
        }}
      >
        Maybe the code hasn't been written yet, or the path was moved during an ecosystem update.
      </p>

      <Link to="/" className="btn btn-primary">
        <ArrowLeft size={16} />
        <span>Return to Clarity</span>
      </Link>
    </div>
  );
};
