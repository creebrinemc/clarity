import React, { useEffect } from 'react';

interface SEOProps {
  title?: string;
  description?: string;
  canonicalPath?: string;
  ogType?: string;
}

const CANONICAL_BASE = 'https://clarity.creebrine.com';
const DEFAULT_TITLE = 'Clarity — Code that speaks for itself';
const DEFAULT_DESCRIPTION =
  'Clarity is a general-purpose programming language designed around readable, expressive syntax without sacrificing structural certainty or future power.';

export const SEO: React.FC<SEOProps> = ({
  title,
  description = DEFAULT_DESCRIPTION,
  canonicalPath = '',
  ogType = 'website',
}) => {
  useEffect(() => {
    // 1. Page Title
    let fullTitle = DEFAULT_TITLE;
    if (title) {
      fullTitle = title.includes('Clarity') ? title : `${title} — Clarity`;
    }
    document.title = fullTitle;

    // 2. Meta Helper
    const setMetaTag = (attrName: string, attrVal: string, content: string) => {
      let element = document.querySelector(`meta[${attrName}="${attrVal}"]`) as HTMLMetaElement;
      if (!element) {
        element = document.createElement('meta');
        element.setAttribute(attrName, attrVal);
        document.head.appendChild(element);
      }
      element.setAttribute('content', content);
    };

    // 3. Description
    setMetaTag('name', 'description', description);

    // 4. OpenGraph
    const cleanPath = canonicalPath.startsWith('/') ? canonicalPath : (canonicalPath ? `/${canonicalPath}` : '');
    const canonicalUrl = `${CANONICAL_BASE}${cleanPath}`;
    setMetaTag('property', 'og:title', fullTitle);
    setMetaTag('property', 'og:description', description);
    setMetaTag('property', 'og:url', canonicalUrl);
    setMetaTag('property', 'og:type', ogType);

    // 5. Twitter
    setMetaTag('property', 'twitter:title', fullTitle);
    setMetaTag('property', 'twitter:description', description);

    // 6. Canonical Link Tag
    let canonicalLink = document.querySelector('link[rel="canonical"]') as HTMLLinkElement;
    if (!canonicalLink) {
      canonicalLink = document.createElement('link');
      canonicalLink.setAttribute('rel', 'canonical');
      document.head.appendChild(canonicalLink);
    }
    canonicalLink.setAttribute('href', canonicalUrl);
  }, [title, description, canonicalPath, ogType]);

  return null;
};

