import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowUpRight, Terminal } from 'lucide-react';
import { GithubIcon } from './GithubIcon';

export const Footer: React.FC = () => (
  <footer className="site-footer">
    <div className="container">
      <div className="footer-main">
        <div className="footer-brand">
          <Link to="/" className="footer-brand-link">
            <span className="brand-mark" aria-hidden="true"><Terminal size={17} /></span>
            <span>Clarity</span>
          </Link>
          <p>Code that speaks for itself. A general-purpose programming language built around readable syntax, predictable structure, and an expanding ecosystem.</p>
          <span className="footer-license">Open source · MIT License · 0.6.0 released</span>
        </div>

        <div className="footer-column">
          <h2>Learn</h2>
          <Link to="/docs/getting-started">Getting started</Link>
          <Link to="/docs/language">Language guide</Link>
          <Link to="/docs/standard-library">Standard library</Link>
          <Link to="/examples">Examples</Link>
        </div>

        <div className="footer-column">
          <h2>Build</h2>
          <Link to="/install">Install Clarity</Link>
          <Link to="/docs/ecosystem">Ecosystem architecture</Link>
          <Link to="/roadmap">Roadmap</Link>
          <a href="https://github.com/creebrinemc/clarity/releases" target="_blank" rel="noopener noreferrer">Releases <ArrowUpRight size={13} /></a>
        </div>

        <div className="footer-column">
          <h2>Project</h2>
          <a href="https://github.com/creebrinemc/clarity" target="_blank" rel="noopener noreferrer"><GithubIcon size={15} /> GitHub repository</a>
          <a href="https://github.com/creebrinemc/clarity/issues" target="_blank" rel="noopener noreferrer">Issue tracker <ArrowUpRight size={13} /></a>
          <a href="https://github.com/creebrinemc/clarity/blob/main/CHANGELOG.md" target="_blank" rel="noopener noreferrer">Changelog <ArrowUpRight size={13} /></a>
        </div>
      </div>

      <div className="footer-bottom">
        <span>Clarity · An open-source programming language project</span>
        <span>clarity.creebrine.com</span>
      </div>
    </div>
  </footer>
);

export default Footer;
