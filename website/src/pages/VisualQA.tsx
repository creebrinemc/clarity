import React, { useState, useEffect } from 'react';
import {
  Monitor,
  Smartphone,
  Maximize2,
  ExternalLink,
  Columns,
  Grid,
  CheckCircle2,
  X,
} from 'lucide-react';
import { SEO } from '../components/SEO';

interface QAPage {
  id: string;
  title: string;
  route: string;
  filename: string;
  category: 'Core' | 'Documentation' | 'Showcase' | 'System';
}

const QA_PAGES: QAPage[] = [
  { id: 'home', title: 'Home Page', route: '/', filename: 'home.png', category: 'Core' },
  { id: 'docs', title: 'Docs: Overview', route: '/docs', filename: 'docs.png', category: 'Documentation' },
  { id: 'getting-started', title: 'Docs: Getting Started', route: '/docs/getting-started', filename: 'getting-started.png', category: 'Documentation' },
  { id: 'language', title: 'Docs: Language Guide', route: '/docs/language', filename: 'language.png', category: 'Documentation' },
  { id: 'standard-library', title: 'Docs: Standard Library', route: '/docs/standard-library', filename: 'standard-library.png', category: 'Documentation' },
  { id: 'examples-docs', title: 'Docs: Examples Walkthrough', route: '/docs/examples', filename: 'examples-docs.png', category: 'Documentation' },
  { id: 'ecosystem', title: 'Docs: Ecosystem Architecture', route: '/docs/ecosystem', filename: 'ecosystem.png', category: 'Documentation' },
  { id: 'spec', title: 'Docs: Formal Specification', route: '/docs/spec', filename: 'spec.png', category: 'Documentation' },
  { id: 'examples', title: 'Examples Showcase', route: '/examples', filename: 'examples.png', category: 'Showcase' },
  { id: 'install', title: 'Installation Guide', route: '/install', filename: 'install.png', category: 'Core' },
  { id: 'roadmap', title: 'Project Roadmap', route: '/roadmap', filename: 'roadmap.png', category: 'Core' },
  { id: 'not-found', title: '404 Error State', route: '/this-does-not-exist', filename: 'not-found.png', category: 'System' },
];

export const VisualQA: React.FC = () => {
  const [viewMode, setViewMode] = useState<'all' | 'desktop' | 'mobile' | 'comparison'>('comparison');
  const [selectedImage, setSelectedImage] = useState<{ url: string; title: string; type: string } | null>(null);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setSelectedImage(null);
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <div style={{ padding: '40px 24px 100px', maxWidth: '1400px', margin: '0 auto' }}>
      <SEO
        title="Visual QA Gallery"
        description="Temporary visual design quality review gallery for Clarity website."
        canonicalPath="/visual-qa"
        noIndex={true}
      />

      {/* Header Banner */}
      <div
        style={{
          borderBottom: '1px solid var(--border-subtle)',
          paddingBottom: '32px',
          marginBottom: '40px',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '12px' }}>
          <span className="badge badge-success">
            <CheckCircle2 size={13} style={{ marginRight: '4px' }} />
            Internal QA System
          </span>
          <span className="badge" style={{ background: 'rgba(129, 140, 248, 0.1)', color: 'var(--accent-purple)' }}>
            Rendered with Google Chrome
          </span>
        </div>

        <h1 style={{ fontSize: '2.5rem', marginBottom: '12px' }}>
          Clarity Website Visual QA Gallery
        </h1>
        <p style={{ fontSize: '1.1rem', color: 'var(--text-secondary)', maxWidth: '800px', lineHeight: 1.6 }}>
          Live browser captures of every official Clarity route across desktop (1440 × 1000) and mobile (390 × 844) viewports. Real fonts, syntax highlighting, CSS tokens, and responsive layout.
        </p>

        {/* View Controls */}
        <div
          style={{
            display: 'flex',
            flexWrap: 'wrap',
            gap: '12px',
            alignItems: 'center',
            marginTop: '28px',
          }}
        >
          <div style={{ display: 'flex', gap: '8px', background: 'var(--bg-surface)', padding: '4px', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)' }}>
            <button
              onClick={() => setViewMode('comparison')}
              className={`btn ${viewMode === 'comparison' ? 'btn-primary' : 'btn-ghost'}`}
              style={{ fontSize: '0.85rem', padding: '6px 14px', gap: '6px' }}
            >
              <Columns size={15} />
              <span>Side-by-Side Comparison</span>
            </button>
            <button
              onClick={() => setViewMode('desktop')}
              className={`btn ${viewMode === 'desktop' ? 'btn-primary' : 'btn-ghost'}`}
              style={{ fontSize: '0.85rem', padding: '6px 14px', gap: '6px' }}
            >
              <Monitor size={15} />
              <span>Desktop Only (1440 × 1000)</span>
            </button>
            <button
              onClick={() => setViewMode('mobile')}
              className={`btn ${viewMode === 'mobile' ? 'btn-primary' : 'btn-ghost'}`}
              style={{ fontSize: '0.85rem', padding: '6px 14px', gap: '6px' }}
            >
              <Smartphone size={15} />
              <span>Mobile Only (390 × 844)</span>
            </button>
            <button
              onClick={() => setViewMode('all')}
              className={`btn ${viewMode === 'all' ? 'btn-primary' : 'btn-ghost'}`}
              style={{ fontSize: '0.85rem', padding: '6px 14px', gap: '6px' }}
            >
              <Grid size={15} />
              <span>All Grid (24 captures)</span>
            </button>
          </div>
        </div>
      </div>

      {/* Side-by-Side Comparison Mode */}
      {viewMode === 'comparison' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '60px' }}>
          {QA_PAGES.map((page) => (
            <div
              key={page.id}
              className="card"
              style={{
                background: 'var(--bg-surface)',
                border: '1px solid var(--border-medium)',
                borderRadius: 'var(--radius-lg)',
                padding: '24px',
              }}
            >
              <div
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  marginBottom: '20px',
                  borderBottom: '1px solid var(--border-subtle)',
                  paddingBottom: '16px',
                }}
              >
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <h2 style={{ fontSize: '1.4rem' }}>{page.title}</h2>
                    <span className="badge" style={{ fontSize: '0.72rem' }}>{page.category}</span>
                  </div>
                  <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.85rem', color: 'var(--accent)', marginTop: '4px' }}>
                    {page.route}
                  </div>
                </div>

                <a
                  href={page.route}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn btn-secondary"
                  style={{ fontSize: '0.82rem', padding: '6px 12px', gap: '6px' }}
                >
                  <ExternalLink size={14} />
                  <span>Open Live Route</span>
                </a>
              </div>

              {/* Two Column Layout: Desktop + Mobile */}
              <div
                style={{
                  display: 'grid',
                  gridTemplateColumns: 'minmax(0, 2.4fr) minmax(0, 1fr)',
                  gap: '24px',
                  alignItems: 'start',
                }}
              >
                {/* Desktop Preview */}
                <div>
                  <div
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      marginBottom: '8px',
                      fontSize: '0.82rem',
                      color: 'var(--text-secondary)',
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                      <Monitor size={14} color="#38bdf8" />
                      <strong style={{ color: 'var(--text-primary)' }}>Desktop</strong> (1440 × 1000)
                    </div>
                    <button
                      onClick={() => setSelectedImage({ url: `/visual-qa/desktop/${page.filename}`, title: page.title, type: 'Desktop (1440 × 1000)' })}
                      className="btn-ghost"
                      style={{ fontSize: '0.78rem', padding: '2px 8px', cursor: 'pointer', gap: '4px' }}
                    >
                      <Maximize2 size={12} />
                      <span>Zoom Fullscreen</span>
                    </button>
                  </div>

                  <div
                    onClick={() => setSelectedImage({ url: `/visual-qa/desktop/${page.filename}`, title: page.title, type: 'Desktop (1440 × 1000)' })}
                    style={{
                      borderRadius: 'var(--radius-md)',
                      overflow: 'hidden',
                      border: '1px solid var(--border-subtle)',
                      background: '#080a0f',
                      cursor: 'zoom-in',
                      aspectRatio: '1440 / 1000',
                    }}
                  >
                    <img
                      src={`/visual-qa/desktop/${page.filename}`}
                      alt={`${page.title} - Desktop 1440x1000`}
                      style={{ width: '100%', height: '100%', objectFit: 'cover', display: 'block' }}
                      loading="lazy"
                    />
                  </div>
                </div>

                {/* Mobile Preview */}
                <div>
                  <div
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      marginBottom: '8px',
                      fontSize: '0.82rem',
                      color: 'var(--text-secondary)',
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                      <Smartphone size={14} color="#818cf8" />
                      <strong style={{ color: 'var(--text-primary)' }}>Mobile</strong> (390 × 844)
                    </div>
                    <button
                      onClick={() => setSelectedImage({ url: `/visual-qa/mobile/${page.filename}`, title: page.title, type: 'Mobile (390 × 844)' })}
                      className="btn-ghost"
                      style={{ fontSize: '0.78rem', padding: '2px 8px', cursor: 'pointer', gap: '4px' }}
                    >
                      <Maximize2 size={12} />
                      <span>Zoom</span>
                    </button>
                  </div>

                  <div
                    onClick={() => setSelectedImage({ url: `/visual-qa/mobile/${page.filename}`, title: page.title, type: 'Mobile (390 × 844)' })}
                    style={{
                      borderRadius: 'var(--radius-md)',
                      overflow: 'hidden',
                      border: '1px solid var(--border-subtle)',
                      background: '#080a0f',
                      cursor: 'zoom-in',
                      aspectRatio: '390 / 844',
                      maxWidth: '340px',
                    }}
                  >
                    <img
                      src={`/visual-qa/mobile/${page.filename}`}
                      alt={`${page.title} - Mobile 390x844`}
                      style={{ width: '100%', height: '100%', objectFit: 'cover', display: 'block' }}
                      loading="lazy"
                    />
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Desktop Only / Mobile Only / All Grid Mode */}
      {viewMode !== 'comparison' && (
        <div
          style={{
            display: 'grid',
            gridTemplateColumns:
              viewMode === 'mobile'
                ? 'repeat(auto-fill, minmax(260px, 1fr))'
                : 'repeat(auto-fill, minmax(420px, 1fr))',
            gap: '28px',
          }}
        >
          {QA_PAGES.map((page) => {
            const showDesktop = viewMode === 'all' || viewMode === 'desktop';
            const showMobile = viewMode === 'all' || viewMode === 'mobile';

            return (
              <React.Fragment key={page.id}>
                {showDesktop && (
                  <div className="card" style={{ padding: '16px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px', fontSize: '0.85rem' }}>
                      <strong>{page.title}</strong>
                      <span className="badge" style={{ fontSize: '0.68rem' }}>1440 × 1000</span>
                    </div>
                    <div
                      onClick={() => setSelectedImage({ url: `/visual-qa/desktop/${page.filename}`, title: page.title, type: 'Desktop (1440 × 1000)' })}
                      style={{ cursor: 'zoom-in', borderRadius: '6px', overflow: 'hidden', border: '1px solid var(--border-subtle)' }}
                    >
                      <img
                        src={`/visual-qa/desktop/${page.filename}`}
                        alt={`${page.title} Desktop`}
                        style={{ width: '100%', display: 'block' }}
                        loading="lazy"
                      />
                    </div>
                  </div>
                )}

                {showMobile && (
                  <div className="card" style={{ padding: '16px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px', fontSize: '0.85rem' }}>
                      <strong>{page.title}</strong>
                      <span className="badge" style={{ fontSize: '0.68rem', color: 'var(--accent-purple)' }}>390 × 844</span>
                    </div>
                    <div
                      onClick={() => setSelectedImage({ url: `/visual-qa/mobile/${page.filename}`, title: page.title, type: 'Mobile (390 × 844)' })}
                      style={{ cursor: 'zoom-in', borderRadius: '6px', overflow: 'hidden', border: '1px solid var(--border-subtle)' }}
                    >
                      <img
                        src={`/visual-qa/mobile/${page.filename}`}
                        alt={`${page.title} Mobile`}
                        style={{ width: '100%', display: 'block' }}
                        loading="lazy"
                      />
                    </div>
                  </div>
                )}
              </React.Fragment>
            );
          })}
        </div>
      )}

      {/* Fullscreen Lightbox Modal */}
      {selectedImage && (
        <div
          onClick={() => setSelectedImage(null)}
          style={{
            position: 'fixed',
            inset: 0,
            zIndex: 99999,
            backgroundColor: 'rgba(0, 0, 0, 0.92)',
            backdropFilter: 'blur(8px)',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '24px',
          }}
        >
          <div
            onClick={(e) => e.stopPropagation()}
            style={{
              position: 'relative',
              maxWidth: '96vw',
              maxHeight: '92vh',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
            }}
          >
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                width: '100%',
                marginBottom: '12px',
                color: 'white',
              }}
            >
              <div>
                <strong style={{ fontSize: '1.1rem' }}>{selectedImage.title}</strong>
                <span className="badge" style={{ marginLeft: '10px' }}>{selectedImage.type}</span>
              </div>
              <button
                onClick={() => setSelectedImage(null)}
                className="btn btn-secondary"
                style={{ padding: '6px 12px', fontSize: '0.85rem', gap: '4px' }}
              >
                <X size={16} />
                <span>Close (Esc)</span>
              </button>
            </div>

            <div
              style={{
                borderRadius: '10px',
                overflow: 'auto',
                border: '1px solid rgba(255, 255, 255, 0.2)',
                boxShadow: '0 20px 50px rgba(0,0,0,0.8)',
                maxHeight: '84vh',
              }}
            >
              <img
                src={selectedImage.url}
                alt={selectedImage.title}
                style={{ display: 'block', maxWidth: '100%', maxHeight: '84vh', objectFit: 'contain' }}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default VisualQA;
