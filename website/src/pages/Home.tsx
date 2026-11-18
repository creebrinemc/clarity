import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import {
  ArrowRight, ArrowUpRight, BookOpen, Braces, CheckCircle2, Code2,
  Compass, GraduationCap, Layers, Monitor, Network, Package,
  ShieldCheck, Sparkles, Terminal, Workflow, Zap,
} from 'lucide-react';
import { GithubIcon } from '../components/GithubIcon';
import { CodeBlock } from '../components/CodeBlock';
import { SEO } from '../components/SEO';

const SYNTAX_TABS = [
  {
    id: 'basics',
    label: 'Readable syntax',
    filename: 'welcome.clr',
    code: [
      'set project to "Clarity"',
      'set score to 96',
      '',
      'if score is at least 90 {',
      '    say "Ready to build with " + project',
      '}',
    ].join('\n'),
    output: 'Ready to build with Clarity',
    note: 'English-inspired phrases make intent easier to scan, while the parser keeps every expression precise.',
  },
  {
    id: 'functions',
    label: 'Functions',
    filename: 'pricing.clr',
    code: [
      'function apply_discount taking price and rate {',
      '    return price * (1 - rate)',
      '}',
      '',
      'set final_price to apply_discount(120, 0.15)',
      'say final_price',
    ].join('\n'),
    output: '102',
    note: 'Named parameter chains and first-class functions give structure to reusable logic.',
  },
  {
    id: 'collections',
    label: 'Data & collections',
    filename: 'inventory.clr',
    code: [
      'set inventory to {',
      '    items: ["Keyboard", "Mouse"],',
      '    count: 2',
      '}',
      '',
      'push "Monitor" to inventory["items"]',
      'say inventory.items',
    ].join('\n'),
    output: '[Keyboard, Mouse, Monitor]',
    note: 'Lists, dictionaries, indexed mutation, and dot access make everyday data work direct.',
  },
  {
    id: 'projects',
    label: 'Projects',
    filename: 'conf.clr',
    code: [
      '{',
      '    name: "starter-project",',
      '    version: "1.0.0",',
      '    entry: "main.clr",',
      '}',
      '',
      '# Run and test from the project root',
      '# clarity run',
      '# clarity test',
    ].join('\n'),
    output: 'Project manifest · conf.clr',
    note: 'A static project manifest connects source files to repeatable run and test workflows.',
  },
];

const PILLARS = [
  {
    icon: <Compass size={22} />,
    title: 'Readable without being vague',
    copy: 'Clarity favors expressive phrases such as “is at least” and “taking … and …”. The syntax aims to explain intent without turning every line into a sentence.',
  },
  {
    icon: <ShieldCheck size={22} />,
    title: 'A real language underneath',
    copy: 'Readable syntax is backed by a lexer, parser, AST, explicit runtime semantics, predictable scope rules, and diagnostics with source locations.',
  },
  {
    icon: <Workflow size={22} />,
    title: 'Useful developer workflows',
    copy: 'The language is paired with a CLI, project manifests, modules, a native test runner, a standard library, and a growing toolchain.',
  },
  {
    icon: <Layers size={22} />,
    title: 'Built as an ecosystem',
    copy: 'Editor support and learning tools share the language server and core semantics instead of becoming disconnected one-off implementations.',
  },
];

const AVAILABLE = [
  {
    icon: <Braces size={20} />,
    title: 'Language core',
    status: 'Released in 0.6.0',
    detail: 'Variables, control flow, functions, closures, collections, modules, imports, dot access, and a practical standard library.',
  },
  {
    icon: <Terminal size={20} />,
    title: 'CLI & project workflow',
    status: 'Released in 0.6.0',
    detail: 'Run source files and projects, scaffold with clarity new, and execute project tests through clarity test.',
  },
  {
    icon: <Package size={20} />,
    title: 'Standalone distribution',
    status: 'Windows available',
    detail: 'A standalone Windows installer is shipped. macOS and Linux native packages remain future work.',
  },
  {
    icon: <Code2 size={20} />,
    title: 'Developer tooling',
    status: '0.7.0 development',
    detail: 'The formatter, static checker, language server, and editor integrations are being developed and verified locally; they are not part of the 0.6.0 release.',
  },
];

const VISION = [
  {
    icon: <Network size={22} />,
    name: 'Clarity Bridge',
    status: 'Planned',
    description: 'Interoperability between languages through a shared intermediate representation, with semantic differences made explicit rather than hidden.',
  },
  {
    icon: <Monitor size={22} />,
    name: 'Clarity Remote',
    status: 'Planned',
    description: 'A secure way to send authorized development tasks to your own computers, queue work while a device is offline, and review what ran.',
  },
  {
    icon: <GraduationCap size={22} />,
    name: 'Teach Me Clarity',
    status: 'Planned',
    description: 'An adaptive learning experience grounded in the language and the project being explored, including source-aware guides such as LEARN.md.',
  },
  {
    icon: <Zap size={22} />,
    name: 'Clarity Playground',
    status: 'Planned',
    description: 'A browser-based, sandboxed place to write and run Clarity snippets, understand diagnostics, and share small experiments.',
  },
];

export const Home: React.FC = () => {
  const [activeTab, setActiveTab] = useState('basics');
  const activeExample = SYNTAX_TABS.find((tab) => tab.id === activeTab) ?? SYNTAX_TABS[0];

  const handleTabKeyDown = (event: React.KeyboardEvent<HTMLDivElement>) => {
    const currentIndex = SYNTAX_TABS.findIndex((tab) => tab.id === activeTab);
    let nextIndex = currentIndex;
    if (event.key === 'ArrowRight' || event.key === 'ArrowDown') nextIndex = (currentIndex + 1) % SYNTAX_TABS.length;
    else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') nextIndex = (currentIndex - 1 + SYNTAX_TABS.length) % SYNTAX_TABS.length;
    else if (event.key === 'Home') nextIndex = 0;
    else if (event.key === 'End') nextIndex = SYNTAX_TABS.length - 1;
    else return;
    event.preventDefault();
    setActiveTab(SYNTAX_TABS[nextIndex].id);
    document.getElementById('syntax-tab-' + SYNTAX_TABS[nextIndex].id)?.focus();
  };

  return (
    <div className="home-page">
      <SEO
        title="Clarity — Code that speaks for itself"
        description="Meet Clarity: a general-purpose programming language built around readable syntax, predictable semantics, and an expanding developer ecosystem."
        canonicalPath="/"
      />

      <section className="site-hero">
        <div className="container">
          <div className="hero-layout">
            <div className="hero-copy">
              <div className="eyebrow">
                <span className="eyebrow-dot" aria-hidden="true" />
                A LANGUAGE. A TOOLCHAIN. A BIGGER IDEA.
              </div>
              <div className="hero-release">
                <span className="release-chip"><CheckCircle2 size={13} /> 0.6.0 released</span>
                <span className="release-separator" aria-hidden="true">/</span>
                <span>0.7.0 in development</span>
              </div>
              <h1 className="hero-title">
                Make the <span>intent</span> obvious.
              </h1>
              <p className="hero-description">
                Clarity is a general-purpose programming language designed to read like structured English without becoming unnecessarily verbose. It pairs expressive syntax with a real language engine—and a developer ecosystem designed to grow around it.
              </p>
              <div className="hero-actions">
                <Link to="/docs/getting-started" className="btn btn-primary">
                  <BookOpen size={17} /> Start with Clarity <ArrowRight size={15} />
                </Link>
                <Link to="/install" className="btn btn-secondary">
                  <Package size={17} /> Installation
                </Link>
                <a href="https://github.com/creebrinemc/clarity" target="_blank" rel="noopener noreferrer" className="btn btn-ghost">
                  <GithubIcon size={17} /> Source code <ArrowUpRight size={14} />
                </a>
              </div>
              <div className="hero-facts" aria-label="Project facts">
                <div><strong>.clr</strong><span>source files</span></div>
                <div><strong>conf.clr</strong><span>project manifest</span></div>
                <div><strong>MIT</strong><span>open source</span></div>
              </div>
            </div>
            <div className="hero-code">
              <div className="hero-code-heading">
                <span className="hero-code-label"><span className="eyebrow-dot" aria-hidden="true" /> A small look at the language</span>
                <span className="hero-code-extension">.clr</span>
              </div>
              <CodeBlock
                code={[
                  '# welcome.clr',
                  'set project to {',
                  '    name: "Clarity",',
                  '    score: 96',
                  '}',
                  '',
                  'function welcome taking item {',
                  '    say "Building with " + item.name',
                  '}',
                  '',
                  'if project.score is at least 90 {',
                  '    welcome(project)',
                  '}',
                ].join('\n')}
                filename="welcome.clr"
                output="Building with Clarity"
              />
              <div className="code-caption">
                <span><CheckCircle2 size={14} /> Structured syntax</span>
                <span><CheckCircle2 size={14} /> Predictable execution</span>
              </div>
            </div>
          </div>
          <div className="hero-bottomline">
            <span>Readable by design</span><i aria-hidden="true" />
            <span>Structured at its core</span><i aria-hidden="true" />
            <span>Designed to grow</span>
          </div>
        </div>
      </section>

      <section className="section" aria-labelledby="why-clarity">
        <div className="container">
          <div className="section-heading">
            <span className="section-kicker">THE REASON IT EXISTS</span>
            <h2 id="why-clarity">Clarity is more than friendly-looking syntax.</h2>
            <p>
              A language should help people understand what a program is doing—not just make its punctuation look different. Clarity brings readability, explicit structure, and practical developer workflows into one coherent design.
            </p>
          </div>
          <div className="pillar-grid">
            {PILLARS.map((item) => (
              <article className="pillar-card" key={item.title}>
                <div className="pillar-icon" aria-hidden="true">{item.icon}</div>
                <h3>{item.title}</h3>
                <p>{item.copy}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="section syntax-section" aria-labelledby="syntax-title">
        <div className="container">
          <div className="split-heading">
            <div>
              <span className="section-kicker">THE LANGUAGE, IN PRACTICE</span>
              <h2 id="syntax-title">See what the words mean.</h2>
            </div>
            <p>Clarity uses familiar ideas with deliberate syntax. Explore a few pieces of the language, then open the examples and documentation to go deeper.</p>
          </div>
          <div className="syntax-showcase">
            <div className="syntax-tabs" role="tablist" aria-label="Clarity language examples" onKeyDown={handleTabKeyDown}>
              {SYNTAX_TABS.map((tab) => (
                <button
                  key={tab.id}
                  type="button"
                  id={'syntax-tab-' + tab.id}
                  role="tab"
                  aria-selected={activeTab === tab.id}
                  aria-controls="syntax-panel"
                  tabIndex={activeTab === tab.id ? 0 : -1}
                  className={activeTab === tab.id ? 'syntax-tab active' : 'syntax-tab'}
                  onClick={() => setActiveTab(tab.id)}
                >
                  {tab.label}
                </button>
              ))}
            </div>
            <div className="syntax-content" id="syntax-panel" role="tabpanel" aria-labelledby={'syntax-tab-' + activeTab} tabIndex={0}>
              <div className="syntax-description">
                <span className="syntax-file">{activeExample.filename}</span>
                <p>{activeExample.note}</p>
              </div>
              <CodeBlock code={activeExample.code} filename={activeExample.filename} output={activeExample.output} />
            </div>
          </div>
          <div className="center-link">
            <Link to="/examples" className="text-link">Explore the examples <ArrowRight size={15} /></Link>
            <Link to="/docs/language" className="text-link">Read the language guide <ArrowRight size={15} /></Link>
          </div>
        </div>
      </section>

      <section className="section" aria-labelledby="available-title">
        <div className="container">
          <div className="split-heading">
            <div>
              <span className="section-kicker">WHAT EXISTS TODAY</span>
              <h2 id="available-title">A working foundation, not a mockup.</h2>
            </div>
            <p>The public 0.6.0 release is the baseline. New toolchain work is being built and tested in 0.7.0 development, with release status kept separate.</p>
          </div>
          <div className="available-grid">
            {AVAILABLE.map((item) => (
              <article className="available-card" key={item.title}>
                <div className="available-card-top">
                  <span className="feature-icon" aria-hidden="true">{item.icon}</span>
                  <span className="status-text">{item.status}</span>
                </div>
                <h3>{item.title}</h3>
                <p>{item.detail}</p>
              </article>
            ))}
          </div>
          <div className="toolchain-note">
            <div className="toolchain-note-icon"><Sparkles size={19} /></div>
            <div>
              <strong>0.7.0 is where the developer workflow expands.</strong>
              <p>Formatting, static analysis, language-server support, and editor integrations are implemented in the current development work. They are not advertised as released features until a version containing them is published.</p>
            </div>
            <Link to="/roadmap" className="text-link">Track progress <ArrowRight size={15} /></Link>
          </div>
        </div>
      </section>

      <section className="section vision-section" aria-labelledby="vision-title">
        <div className="container">
          <div className="section-heading">
            <span className="section-kicker">THE LONGER-TERM VISION</span>
            <h2 id="vision-title">One connected development experience.</h2>
            <p>
              The ambition is not a collection of unrelated utilities. It is a connected environment where the language, tools, learning, remote work, and integrations understand the same project and the same source of truth.
            </p>
          </div>

          <div className="vision-hub">
            <div className="vision-hub-core">
              <div className="vision-hub-mark"><Terminal size={23} /></div>
              <div><strong>Clarity</strong><span>Language + shared intelligence</span></div>
            </div>
            <div className="vision-hub-grid">
              {VISION.map((item) => (
                <article className="vision-card" key={item.name}>
                  <div className="vision-card-head">
                    <span className="feature-icon" aria-hidden="true">{item.icon}</span>
                    <span className="future-label">{item.status}</span>
                  </div>
                  <h3>{item.name}</h3>
                  <p>{item.description}</p>
                </article>
              ))}
            </div>
            <div className="vision-unified">
              <div className="vision-unified-icon"><Layers size={21} /></div>
              <div>
                <span className="section-kicker">UNIFIED DEVELOPMENT APPLICATION · CONCEPT DIRECTION</span>
                <h3>A single workspace for building with Clarity.</h3>
                <p>An integrated editor, AI development agent, project workspace, debugging and language intelligence, terminal, tests, builds, packaging, learning, and remote development—designed to work together across desktop, web, and mobile.</p>
              </div>
            </div>
          </div>
          <p className="vision-footnote">These are long-term directions, not promises of availability or release dates. Product naming and implementation details may evolve.</p>
        </div>
      </section>

      <section className="section" aria-labelledby="principles-title">
        <div className="container principles-layout">
          <div>
            <span className="section-kicker">WHY BUILD WITH CLARITY?</span>
            <h2 id="principles-title">Less time decoding. More time creating.</h2>
            <p className="principles-intro">Clarity is for developers who value code that communicates intent, a language implementation they can inspect, and tools that grow from the same foundations.</p>
          </div>
          <div className="principles-list">
            <div><span>01</span><p><strong>Read the program as a program.</strong> Expressive keywords and comparison phrases put intent closer to the surface.</p></div>
            <div><span>02</span><p><strong>Keep the structure explicit.</strong> A real parser, AST, runtime, modules, and project model provide the foundations behind the syntax.</p></div>
            <div><span>03</span><p><strong>Grow with the ecosystem.</strong> Start with the language and CLI; add editor, learning, and workflow tools as they mature.</p></div>
          </div>
        </div>
      </section>

      <section className="final-cta">
        <div className="container final-cta-inner">
          <div>
            <span className="section-kicker">YOUR NEXT STEP</span>
            <h2>Give your ideas a clearer way to run.</h2>
            <p>Start with the language, explore the docs, or follow the work as the ecosystem develops.</p>
          </div>
          <div className="hero-actions">
            <Link to="/install" className="btn btn-primary"><Package size={17} /> Get Clarity <ArrowRight size={15} /></Link>
            <Link to="/roadmap" className="btn btn-secondary">Explore the roadmap</Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
