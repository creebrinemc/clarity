import React, { useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Menu, X, Terminal } from 'lucide-react';
import { GithubIcon } from './GithubIcon';

const NAV_LINKS = [
  { label: 'Docs', path: '/docs' },
  { label: 'Examples', path: '/examples' },
  { label: 'Install', path: '/install' },
  { label: 'Roadmap', path: '/roadmap' },
];

export const Navbar: React.FC = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const location = useLocation();

  useEffect(() => {
    const handleScroll = () => setIsScrolled(window.scrollY > 12);
    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    setMobileMenuOpen(false);
  }, [location.pathname]);

  useEffect(() => {
    if (!mobileMenuOpen) return;
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') setMobileMenuOpen(false);
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [mobileMenuOpen]);

  const isActive = (path: string) => path === '/docs'
    ? location.pathname.startsWith('/docs')
    : location.pathname === path;

  return (
    <header className={isScrolled ? 'site-header is-scrolled' : 'site-header'}>
      <div className="container navbar-inner">
        <Link to="/" className="brand-link" aria-label="Clarity home">
          <span className="brand-mark" aria-hidden="true"><Terminal size={18} strokeWidth={2.5} /></span>
          <span className="brand-name">Clarity</span>
          <span className="brand-version">0.6.0</span>
        </Link>

        <nav className="desktop-nav" aria-label="Main navigation">
          {NAV_LINKS.map((link) => (
            <Link key={link.path} to={link.path} aria-current={isActive(link.path) ? 'page' : undefined} className={isActive(link.path) ? 'nav-link active' : 'nav-link'}>
              {link.label}
            </Link>
          ))}
          <a href="https://github.com/creebrinemc/clarity" target="_blank" rel="noopener noreferrer" className="btn btn-secondary nav-github" aria-label="Clarity on GitHub, opens in a new tab">
            <GithubIcon size={15} /> GitHub
          </a>
        </nav>

        <button
          className="mobile-toggle"
          type="button"
          onClick={() => setMobileMenuOpen((open) => !open)}
          aria-label={mobileMenuOpen ? 'Close navigation menu' : 'Open navigation menu'}
          aria-expanded={mobileMenuOpen}
          aria-controls="mobile-navigation"
        >
          {mobileMenuOpen ? <X size={22} aria-hidden="true" /> : <Menu size={22} aria-hidden="true" />}
        </button>
      </div>

      {mobileMenuOpen && (
        <nav className="mobile-nav" id="mobile-navigation" aria-label="Mobile navigation">
          {NAV_LINKS.map((link) => (
            <Link key={link.path} to={link.path} aria-current={isActive(link.path) ? 'page' : undefined} className={isActive(link.path) ? 'mobile-nav-link active' : 'mobile-nav-link'}>
              {link.label}
            </Link>
          ))}
          <a href="https://github.com/creebrinemc/clarity" target="_blank" rel="noopener noreferrer" className="btn btn-secondary">
            <GithubIcon size={16} /> View source on GitHub
          </a>
        </nav>
      )}
    </header>
  );
};

export default Navbar;
