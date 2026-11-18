import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, CheckCircle2, Clock3, GitBranch, Sparkles } from 'lucide-react';
import { SEO } from '../components/SEO';

type Status = 'shipped' | 'development' | 'planned';

interface Milestone {
  version: string;
  title: string;
  status: Status;
  description: string;
  highlights: string[];
  footnote?: string;
}

const MILESTONES: Milestone[] = [
  {
    version: '0.1.0',
    title: 'Core language foundation',
    status: 'shipped',
    description: 'The initial language established the foundations for expressing and evaluating programs.',
    highlights: ['Variable bindings with set … to …', 'Arithmetic and operator precedence', 'say output statement', 'Source spans for useful diagnostics'],
  },
  {
    version: '0.1.1',
    title: 'Foundation hardening',
    status: 'shipped',
    description: 'Lexer and diagnostic improvements made the initial language more robust.',
    highlights: ['Line comments with #', 'Unary operators and logical not', 'Improved line and column diagnostics'],
  },
  {
    version: '0.2.0',
    title: 'Control flow',
    status: 'shipped',
    description: 'Programs gained branching, loops, and explicit loop control.',
    highlights: ['if / else if / else', 'while and numeric range loops', 'break and continue'],
  },
  {
    version: '0.3.0',
    title: 'Functions and closures',
    status: 'shipped',
    description: 'Clarity added first-class functions and lexical closure behavior.',
    highlights: ['taking … and … parameter chains', 'First-class functions and return values', 'Lexical closures, recursion, and nested functions'],
  },
  {
    version: '0.4.0',
    title: 'Data and readability',
    status: 'shipped',
    description: 'Collections and natural-language comparison aliases made the language more expressive.',
    highlights: ['Lists, dictionaries, and 0-based indexing', 'Indexed mutation on lists and dictionaries', 'is at least / is greater than comparison phrases', 'for each and repeat N times'],
  },
  {
    version: '0.5.0',
    title: 'Standard library',
    status: 'shipped',
    description: 'A built-in library added practical text, collection, math, random, and filesystem operations.',
    highlights: ['Text and collection helpers', 'Math operations and random selection', 'UTF-8 filesystem operations', 'Clarity diagnostics instead of leaked host exceptions'],
  },
  {
    version: '0.6.0',
    title: 'Modules and project system',
    status: 'shipped',
    description: 'The 0.6.0 release introduced modular programs and a project-aware workflow.',
    highlights: ['import and from … import with module privacy', 'Static conf.clr project manifest', 'clarity run, clarity new, and clarity test', 'assert / assert_equal and standalone Windows installer'],
  },
  {
    version: '0.7.0',
    title: 'Developer toolchain',
    status: 'development',
    description: 'The active development milestone expands Clarity from a language with a CLI into a language with a connected developer workflow.',
    highlights: [
      'AST-based formatter: clarity format, with check and JSON modes',
      'Static analysis: clarity check without executing the program',
      'Language server: clarity lsp --stdio, including diagnostics, completion, hover, definition, symbols, and formatting',
      'VS Code integration implemented and tested in development work',
      'JetBrains plugin implemented with LSP4IJ, CLI actions, settings, and a Clarity tool window',
    ],
    footnote: 'Development status: the work has been implemented and automated checks have passed locally. The JetBrains plugin still needs interactive IDE smoke testing; the integrations and tooling have not yet been included in a public Clarity release.',
  },
];

const DIRECTION = [
  {
    title: 'Cross-platform distribution',
    status: 'Planned',
    description: 'Native macOS and Linux packages to complement the existing Windows installer. Source installation remains available today.',
  },
  {
    title: 'A richer learning layer',
    status: 'Planned',
    description: 'Teach Me Clarity, interactive learning, project-aware explanations, and source-grounded LEARN.md guides.',
  },
  {
    title: 'An integrated development environment',
    status: 'Long-term direction',
    description: 'A unified workspace combining editing, language intelligence, an AI development agent, project workflows, debugging, builds, tests, and packaging.',
  },
  {
    title: 'Connected ecosystem services',
    status: 'Long-term direction',
    description: 'Clarity Bridge for language interoperability, Clarity Remote for authorized remote workflows, and a sandboxed browser Playground.',
  },
];

const statusLabel: Record<Status, string> = {
  shipped: 'Shipped',
  development: 'In development',
  planned: 'Planned',
};

export const Roadmap: React.FC = () => (
  <div className="roadmap-page">
    <SEO
      title="Clarity Roadmap"
      description="See what has shipped in Clarity, what is being developed for 0.7.0, and the longer-term direction of the ecosystem."
      canonicalPath="/roadmap"
    />
    <section className="roadmap-hero">
      <div className="container">
        <span className="section-kicker">TRANSPARENT PROGRESS</span>
        <h1 className="page-hero-title">The roadmap, without the guesswork.</h1>
        <p>Clarity's roadmap separates released capabilities from work in development and ideas for the longer term. A planned item is a direction—not a release promise.</p>
        <div className="roadmap-legend" aria-label="Roadmap status definitions">
          <span className="status-pill status-shipped"><CheckCircle2 size={14} /> Shipped</span>
          <span className="status-pill status-development"><GitBranch size={14} /> In development</span>
          <span className="status-pill status-planned"><Clock3 size={14} /> Planned</span>
        </div>
      </div>
    </section>

    <section className="section roadmap-section" aria-labelledby="release-history-title">
      <div className="container roadmap-container">
        <div className="roadmap-section-heading">
          <div>
            <span className="section-kicker">RELEASE HISTORY + ACTIVE WORK</span>
            <h2 id="release-history-title">From language core to developer toolchain.</h2>
          </div>
          <p>Milestones are shown by actual project state. 0.6.0 is the latest published release represented here; 0.7.0 remains development work.</p>
        </div>

        <div className="milestone-list">
          {MILESTONES.map((milestone) => (
            <article className={'milestone-card milestone-' + milestone.status} key={milestone.version}>
              <div className="milestone-rail" aria-hidden="true"><span /></div>
              <div className="milestone-body">
                <div className="milestone-topline">
                  <span className="milestone-version">{milestone.version}</span>
                  <span className={'status-pill status-' + milestone.status}>
                    {milestone.status === 'shipped' ? <CheckCircle2 size={14} /> : milestone.status === 'development' ? <Sparkles size={14} /> : <Clock3 size={14} />}
                    {statusLabel[milestone.status]}
                  </span>
                </div>
                <h3>{milestone.title}</h3>
                <p className="milestone-description">{milestone.description}</p>
                <ul className="milestone-highlights">
                  {milestone.highlights.map((item) => <li key={item}>{item}</li>)}
                </ul>
                {milestone.footnote && <p className="milestone-footnote">{milestone.footnote}</p>}
              </div>
            </article>
          ))}
        </div>

        <div className="development-callout">
          <div className="callout-icon"><GitBranch size={20} /></div>
          <div>
            <span className="section-kicker">IMPORTANT RELEASE DISTINCTION</span>
            <h3>Implemented does not mean released.</h3>
            <p>The formatter, checker, LSP, and IDE integrations are part of active 0.7.0 development. They should be treated as development builds until a tagged release and distribution are published.</p>
          </div>
        </div>
      </div>
    </section>

    <section className="section roadmap-direction" aria-labelledby="direction-title">
      <div className="container">
        <div className="roadmap-section-heading">
          <div>
            <span className="section-kicker">BEYOND THE CURRENT MILESTONE</span>
            <h2 id="direction-title">Where the ecosystem can go next.</h2>
          </div>
          <p>These themes describe the intended direction. Their order, scope, and names may change as the core language and tooling mature.</p>
        </div>
        <div className="direction-grid">
          {DIRECTION.map((item) => (
            <article className="direction-card" key={item.title}>
              <div className="direction-status">{item.status}</div>
              <h3>{item.title}</h3>
              <p>{item.description}</p>
            </article>
          ))}
        </div>
      </div>
    </section>

    <section className="roadmap-footer">
      <div className="container roadmap-footer-inner">
        <div>
          <span className="section-kicker">FOLLOW THE IMPLEMENTATION</span>
          <h2>See the code and the release history.</h2>
          <p>The repository and changelog are the source of truth for what is publicly available.</p>
        </div>
        <div className="hero-actions">
          <a className="btn btn-primary" href="https://github.com/creebrinemc/clarity" target="_blank" rel="noopener noreferrer">Open GitHub <ArrowRight size={15} /></a>
          <Link className="btn btn-secondary" to="/install">Get the released version</Link>
        </div>
      </div>
    </section>
  </div>
);

export default Roadmap;
