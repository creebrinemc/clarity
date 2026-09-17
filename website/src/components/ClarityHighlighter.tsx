import React from 'react';

interface Token {
  type:
    | 'keyword'
    | 'phrase'
    | 'builtin'
    | 'string'
    | 'number'
    | 'boolean'
    | 'comment'
    | 'operator'
    | 'punctuation'
    | 'identifier'
    | 'plain';
  text: string;
}

const PHRASES = [
  'is at least',
  'is at most',
  'is greater than',
  'is less than',
  'is equal to',
  'is not equal to',
];

const KEYWORDS = new Set([
  'set',
  'to',
  'say',
  'if',
  'else',
  'while',
  'for',
  'each',
  'in',
  'from',
  'step',
  'repeat',
  'times',
  'function',
  'taking',
  'and',
  'or',
  'not',
  'return',
  'break',
  'continue',
  'push',
  'pop',
]);

const BUILTINS = new Set([
  'length',
  'uppercase',
  'lowercase',
  'trim',
  'contains',
  'replace',
  'split',
  'join',
  'reverse',
  'sort',
  'abs',
  'floor',
  'ceil',
  'round',
  'min',
  'max',
  'sqrt',
  'power',
  'random',
  'choose',
  'read_file',
  'write_file',
  'file_exists',
]);

const BOOLEANS = new Set(['true', 'false', 'nothing', 'null']);

export function tokenizeClarity(line: string): Token[] {
  const tokens: Token[] = [];
  let i = 0;

  while (i < line.length) {
    // 1. Comment
    if (line[i] === '#') {
      tokens.push({ type: 'comment', text: line.slice(i) });
      break;
    }

    // 2. String
    if (line[i] === '"') {
      let j = i + 1;
      while (j < line.length && line[j] !== '"') {
        if (line[j] === '\\' && j + 1 < line.length) {
          j += 2;
        } else {
          j++;
        }
      }
      if (j < line.length && line[j] === '"') j++;
      tokens.push({ type: 'string', text: line.slice(i, j) });
      i = j;
      continue;
    }

    // 3. Multi-word phrases
    let matchedPhrase = false;
    for (const phrase of PHRASES) {
      if (line.slice(i, i + phrase.length) === phrase) {
        // Ensure word boundaries
        const before = i === 0 || /\s|[^\w]/.test(line[i - 1]);
        const nextChar = line[i + phrase.length];
        const after = nextChar === undefined || /\s|[^\w]/.test(nextChar);
        if (before && after) {
          tokens.push({ type: 'phrase', text: phrase });
          i += phrase.length;
          matchedPhrase = true;
          break;
        }
      }
    }
    if (matchedPhrase) continue;

    // 4. Numbers
    if (/\d/.test(line[i])) {
      let j = i;
      while (j < line.length && /[\d.]/.test(line[j])) j++;
      tokens.push({ type: 'number', text: line.slice(i, j) });
      i = j;
      continue;
    }

    // 5. Identifiers & Keywords
    if (/[a-zA-Z_]/.test(line[i])) {
      let j = i;
      while (j < line.length && /[\w]/.test(line[j])) j++;
      const word = line.slice(i, j);

      if (KEYWORDS.has(word)) {
        tokens.push({ type: 'keyword', text: word });
      } else if (BUILTINS.has(word)) {
        tokens.push({ type: 'builtin', text: word });
      } else if (BOOLEANS.has(word)) {
        tokens.push({ type: 'boolean', text: word });
      } else {
        tokens.push({ type: 'identifier', text: word });
      }
      i = j;
      continue;
    }

    // 6. Operators & Punctuation
    if ('+-*/%<>!=&|'.includes(line[i])) {
      let op = line[i];
      if (i + 1 < line.length && ['==', '!=', '>=', '<='].includes(line.slice(i, i + 2))) {
        op = line.slice(i, i + 2);
        i += 2;
      } else {
        i++;
      }
      tokens.push({ type: 'operator', text: op });
      continue;
    }

    if ('{}()[],:'.includes(line[i])) {
      tokens.push({ type: 'punctuation', text: line[i] });
      i++;
      continue;
    }

    // 7. Whitespace / Other
    tokens.push({ type: 'plain', text: line[i] });
    i++;
  }

  return tokens;
}

export const ClarityHighlighter: React.FC<{ code: string; showLineNumbers?: boolean }> = ({
  code,
  showLineNumbers = false,
}) => {
  const lines = code.trimEnd().split('\n');

  return (
    <div className="clarity-code">
      {lines.map((line, idx) => {
        const tokens = tokenizeClarity(line);
        return (
          <div key={idx} className="code-line">
            {showLineNumbers && <span className="line-number">{idx + 1}</span>}
            <span className="line-content">
              {tokens.length === 0 ? (
                '\u00A0'
              ) : (
                tokens.map((token, tIdx) => (
                  <span key={tIdx} className={`token-${token.type}`}>
                    {token.text}
                  </span>
                ))
              )}
            </span>
          </div>
        );
      })}
    </div>
  );
};
