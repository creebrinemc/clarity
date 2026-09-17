import React, { useState } from 'react';
import { Copy, Check, Terminal } from 'lucide-react';
import { ClarityHighlighter } from './ClarityHighlighter';

interface CodeBlockProps {
  code: string;
  filename?: string;
  output?: string;
  showLineNumbers?: boolean;
  className?: string;
}

export const CodeBlock: React.FC<CodeBlockProps> = ({
  code,
  filename = 'main.clr',
  output,
  showLineNumbers = true,
  className = '',
}) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy code: ', err);
    }
  };

  return (
    <div className={`code-window ${className}`} role="region" aria-label={`Code example: ${filename}`}>
      <div className="code-window-header">
        <div className="window-controls" aria-hidden="true">
          <span className="window-dot close" />
          <span className="window-dot minimize" />
          <span className="window-dot expand" />
        </div>
        <div className="window-title">
          <Terminal size={13} style={{ opacity: 0.7 }} aria-hidden="true" />
          <span>{filename}</span>
        </div>
        <button
          onClick={handleCopy}
          className="btn-ghost"
          style={{
            padding: '4px 8px',
            fontSize: '0.78rem',
            borderRadius: '4px',
            gap: '4px',
            cursor: 'pointer',
          }}
          title={copied ? "Copied!" : "Copy code"}
          aria-label={copied ? "Code copied to clipboard" : `Copy code from ${filename} to clipboard`}
        >
          {copied ? (
            <>
              <Check size={13} color="#10b981" aria-hidden="true" />
              <span style={{ color: '#10b981' }}>Copied</span>
            </>
          ) : (
            <>
              <Copy size={13} aria-hidden="true" />
              <span>Copy</span>
            </>
          )}
        </button>
      </div>

      <div className="code-window-body">
        <ClarityHighlighter code={code} showLineNumbers={showLineNumbers} />
      </div>

      {output && (
        <div
          style={{
            borderTop: '1px solid var(--border-subtle)',
            background: 'rgba(0, 0, 0, 0.3)',
            padding: '12px 18px',
            fontSize: '0.85rem',
            fontFamily: 'var(--font-mono)',
          }}
        >
          <div
            style={{
              color: 'var(--text-muted)',
              fontSize: '0.75rem',
              textTransform: 'uppercase',
              letterSpacing: '0.05em',
              marginBottom: '6px',
            }}
          >
            Output
          </div>
          <pre style={{ color: '#38bdf8', whiteSpace: 'pre-wrap', margin: 0 }}>
            {output}
          </pre>
        </div>
      )}
    </div>
  );
};
