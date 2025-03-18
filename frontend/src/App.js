import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';

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
  return (
    <CompanyProvider>
      <div className="App">
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
          <div className="container">
            <Link className="navbar-brand" to="/">Company Themes</Link>
            <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
              <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarNav">
              <ul className="navbar-nav me-auto">
                <li className="nav-item">
                  <Link className="nav-link" to="/">Home</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/themes">Themes</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/questions">Ask Questions</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/documents">Documents</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/add-theme">Add Theme</Link>
                </li>
              </ul>
              <div className="d-flex">
                <CompanySelector />
              </div>
            </div>
          </div>
        </nav>

        <div className="container">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/themes" element={<ThemesPage />} />
            <Route path="/questions" element={<QuestionsPage />} />
            <Route path="/documents" element={<DocumentsPage />} />
            <Route path="/add-theme" element={<AddThemePage />} />
          </Routes>
        </div>

        <footer className="mt-5 py-3 text-center text-muted">
          <div className="container">
            <p>Company Theme Extraction and Question-Answering System &copy; 2025</p>
          </div>
        </footer>
      </div>
    </CompanyProvider>
  );
}

export default App;
