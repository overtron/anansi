import React, { useState, useEffect } from 'react';
import { Routes, Route, Link, useLocation } from 'react-router-dom';

// Import context providers
import { CompanyProvider } from './context/CompanyContext';

// Import components
import CompanySelector from './components/CompanySelector';

// Import pages
import HomePage from './pages/HomePage';
import ThemesPage from './pages/ThemesPage';
import QuestionsPage from './pages/QuestionsPage';
import DocumentsPage from './pages/DocumentsPage';
import AddThemePage from './pages/AddThemePage';

function App() {
  const [scrolled, setScrolled] = useState(false);
  const location = useLocation();

  // Handle navbar transparency on scroll
  useEffect(() => {
    const handleScroll = () => {
      const isScrolled = window.scrollY > 50;
      if (isScrolled !== scrolled) {
        setScrolled(isScrolled);
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, [scrolled]);

  // Reset scroll position on page change
  useEffect(() => {
    window.scrollTo(0, 0);
  }, [location.pathname]);

  return (
    <CompanyProvider>
      <div className="App">
        {/* Modern Netflix-inspired Navbar */}
        <nav className={`netflix-navbar ${scrolled ? 'scrolled' : ''}`}>
          <div className="container-fluid px-4">
            <div className="d-flex justify-content-between align-items-center w-100">
              <div className="d-flex align-items-center">
                <Link className="navbar-brand" to="/">Company Themes</Link>
                <button className="navbar-toggler ms-2 d-lg-none" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                  <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarNav">
                  <ul className="navbar-nav">
                    <li className="nav-item">
                      <Link className={`nav-link ${location.pathname === '/' ? 'active' : ''}`} to="/">Home</Link>
                    </li>
                    <li className="nav-item">
                      <Link className={`nav-link ${location.pathname === '/themes' ? 'active' : ''}`} to="/themes">Themes</Link>
                    </li>
                    <li className="nav-item">
                      <Link className={`nav-link ${location.pathname === '/questions' ? 'active' : ''}`} to="/questions">Ask Questions</Link>
                    </li>
                    <li className="nav-item">
                      <Link className={`nav-link ${location.pathname === '/documents' ? 'active' : ''}`} to="/documents">Documents</Link>
                    </li>
                    <li className="nav-item">
                      <Link className={`nav-link ${location.pathname === '/add-theme' ? 'active' : ''}`} to="/add-theme">Add Theme</Link>
                    </li>
                  </ul>
                </div>
              </div>
              <div className="netflix-company-selector">
                <CompanySelector />
              </div>
            </div>
          </div>
        </nav>

        {/* Main Content Container */}
        <div className="netflix-container">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/themes" element={<ThemesPage />} />
            <Route path="/questions" element={<QuestionsPage />} />
            <Route path="/documents" element={<DocumentsPage />} />
            <Route path="/add-theme" element={<AddThemePage />} />
          </Routes>
        </div>

        {/* Modern Footer */}
        <footer className="netflix-footer">
          <div className="container">
            <div className="row">
              <div className="col-md-6">
                <h5 className="mb-3">Company Theme Analysis</h5>
                <p className="mb-0">Extract business insights from corporate documents</p>
              </div>
              <div className="col-md-6 text-md-end">
                <p className="mb-0">&copy; 2025 Theme Extraction System</p>
              </div>
            </div>
          </div>
        </footer>
      </div>
    </CompanyProvider>
  );
}

export default App;
