# Clarity Website (`website/`)

The official production-ready website and interactive documentation portal for the Clarity programming language.

* **Production URL**: [`https://clarity.creebrine.com`](https://clarity.creebrine.com)
* **Tagline**: *"Clarity — Code that speaks for itself."*
* **Stack**: Vite + React 19 + TypeScript + Custom Clarity Syntax Highlighter + Modern Responsive CSS Design System

---

## Website Structure & Pages

1. **Home (`/`)**:
   - Hero with tagline *"Code that speaks for itself"* and interactive Clarity code editor window (`hello.clr`).
   - "Why Clarity?" design pillars (Readable, Structured, General-purpose, Built to grow).
   - "Readability by Design" side-by-side comparison section.
   - Interactive hands-on Language Showcase (Hello, Functions & Closures, Collections, Control Flow, Standard Library).
   - Platform Architecture & Interactive Ecosystem Diagram.
   - Milestone tracker and open-source GitHub call to action.

2. **Documentation (`/docs`)**:
   - Getting Started Guide (`/docs/getting-started`)
   - Language Guide (`/docs/language`)
   - Standard Library Reference (`/docs/standard-library`)
   - Examples Walkthrough (`/docs/examples`)
   - Ecosystem Architecture (`/docs/ecosystem`)
   - Language Specification (`/docs/spec`)

3. **Examples (`/examples`)**:
   - Categorized gallery (Beginner, Language Features, Standard Library) with copyable real `.clr` code and outputs.

4. **Installation (`/install`)**:
   - Step-by-step development setup instructions with verification commands.
   - Transparent preview of upcoming native installers (Windows `.exe`, macOS `.pkg`/brew, Linux).

5. **Roadmap (`/roadmap`)**:
   - Complete milestone tracker (0.1.0 through 0.5.0 completed, upcoming 0.6.x Modules, Toolchain, Installers, and Editor).

6. **404 Page (`*`)**:
   - Custom, polished not-found state with navigation back to safety.

---

## Local Development & Commands

Run all commands from the `website/` directory:

```bash
# Install dependencies
npm install

# Start local development server
npm run dev

# Build production bundle
npm run build

# Preview production build locally
npm run preview
```

---

## Deployment & Hosting

The website compiles to a static single-page application inside `website/dist/`.

* **Vercel Configuration**: `vercel.json` contains SPA rewrite rules (`/(.*) -> /index.html`), security headers (`X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`), and long-term asset caching headers.
* **Canonical Domain**: `https://clarity.creebrine.com`
* **Sitemap & Robots**: `public/sitemap.xml` and `public/robots.txt` are bundled into the distribution directory for search engine indexing.
* **Dynamic Head Management**: The `<SEO>` component manages per-route page titles, descriptions, canonical links, OpenGraph metadata, and Twitter cards dynamically on route navigation.

