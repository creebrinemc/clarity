import React, { useEffect } from 'react';
import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom';
import { Navbar } from './components/Navbar';
import { Footer } from './components/Footer';
import { Home } from './pages/Home';
import { Docs } from './pages/Docs';
import { Examples } from './pages/Examples';
import { Install } from './pages/Install';
import { Roadmap } from './pages/Roadmap';
import { NotFound } from './pages/NotFound';
import { VisualQA } from './pages/VisualQA';

function ScrollToTop() {
  const { pathname } = useLocation();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);

  return null;
}

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <ScrollToTop />
      <a href="#main-content" className="skip-link">
        Skip to main content
      </a>
      <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
        <Navbar />
        <main id="main-content" style={{ flex: 1 }} tabIndex={-1}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/docs" element={<Docs />} />
            <Route path="/docs/:section" element={<Docs />} />
            <Route path="/examples" element={<Examples />} />
            <Route path="/install" element={<Install />} />
            <Route path="/roadmap" element={<Roadmap />} />
            <Route path="/visual-qa" element={<VisualQA />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </BrowserRouter>
  );
};

export default App;
