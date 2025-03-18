import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useCompany } from '../context/CompanyContext';

const HomePage = () => {
  const { selectedCompany } = useCompany();
  const [stats, setStats] = useState({
    themes: 0,
    documents: 0,
    categories: 0
  });
  
  // Simulate loading stats
  useEffect(() => {
    if (selectedCompany) {
      // In a real app, this would fetch actual stats from an API
      setStats({
        themes: Math.floor(Math.random() * 20) + 10,
        documents: Math.floor(Math.random() * 15) + 5,
        categories: Math.floor(Math.random() * 6) + 3
      });
    }
  }, [selectedCompany]);

  return (
    <div className="home-page netflix-fade-in">
      {/* Hero Section */}
      <div className="netflix-hero">
        <h1>Company Theme Analysis</h1>
        <p>
          Explore business growth and contraction themes extracted from {selectedCompany ? `${selectedCompany.name}'s` : 'company'} investor relations documents and SEC filings.
        </p>
        <div className="d-flex gap-3 mt-4">
          <Link to="/themes" className="netflix-btn netflix-btn-lg">Explore Themes</Link>
          <Link to="/questions" className="netflix-btn netflix-btn-outline netflix-btn-lg">Ask Questions</Link>
        </div>
      </div>

      {/* Stats Cards */}
      {selectedCompany && (
        <div className="row mb-5">
          <div className="col-md-4">
            <div className="netflix-card text-center">
              <div className="netflix-card-body">
                <h2 className="display-4 text-netflix-red">{stats.themes}</h2>
                <p className="text-netflix-white">Business Themes</p>
              </div>
            </div>
          </div>
          <div className="col-md-4">
            <div className="netflix-card text-center">
              <div className="netflix-card-body">
                <h2 className="display-4 text-netflix-red">{stats.documents}</h2>
                <p className="text-netflix-white">Source Documents</p>
              </div>
            </div>
          </div>
          <div className="col-md-4">
            <div className="netflix-card text-center">
              <div className="netflix-card-body">
                <h2 className="display-4 text-netflix-red">{stats.categories}</h2>
                <p className="text-netflix-white">Theme Categories</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Feature Cards */}
      <h2 className="netflix-row-title mb-4">Features</h2>
      <div className="netflix-row-content mb-5">
        <div className="netflix-row-item">
          <div className="netflix-card h-100">
            <div className="netflix-card-header">Theme Exploration</div>
            <div className="netflix-card-body">
              <p>
                Browse through extracted business themes organized by category. Each theme includes supporting evidence from source documents.
              </p>
              <Link to="/themes" className="netflix-btn netflix-btn-sm mt-2">Explore Themes</Link>
            </div>
          </div>
        </div>
        <div className="netflix-row-item">
          <div className="netflix-card h-100">
            <div className="netflix-card-header">Question Answering</div>
            <div className="netflix-card-body">
              <p>
                Ask questions about {selectedCompany ? `${selectedCompany.name}'s` : 'company'} business themes and get AI-powered answers with citations from source documents.
              </p>
              <Link to="/questions" className="netflix-btn netflix-btn-sm mt-2">Ask Questions</Link>
            </div>
          </div>
        </div>
        <div className="netflix-row-item">
          <div className="netflix-card h-100">
            <div className="netflix-card-header">Document Management</div>
            <div className="netflix-card-body">
              <p>
                View the source documents used for theme extraction, including investor relations PDFs and SEC filings.
              </p>
              <Link to="/documents" className="netflix-btn netflix-btn-sm mt-2">View Documents</Link>
            </div>
          </div>
        </div>
        <div className="netflix-row-item">
          <div className="netflix-card h-100">
            <div className="netflix-card-header">Add Custom Themes</div>
            <div className="netflix-card-body">
              <p>
                Manually add custom business themes that you've identified through your own analysis.
              </p>
              <Link to="/add-theme" className="netflix-btn netflix-btn-sm mt-2">Add Theme</Link>
            </div>
          </div>
        </div>
      </div>

      {/* How It Works Section */}
      <div className="netflix-panel mb-5">
        <div className="netflix-panel-header">
          <span>How It Works</span>
        </div>
        <div className="netflix-panel-body">
          <p>
            This system uses OpenAI's GPT-4o model to analyze {selectedCompany ? `${selectedCompany.name}'s` : 'company'} investor relations documents and SEC filings, 
            extracting key business themes related to growth and contraction factors. The themes are categorized and 
            presented with supporting evidence from the source documents.
          </p>
          <p>
            You can also ask questions about the themes, and the system will provide answers based on the source documents,
            with proper citations to help you understand the context.
          </p>
          
          <div className="row mt-4">
            <div className="col-md-4 text-center">
              <div className="mb-3">
                <i className="fas fa-file-alt text-netflix-red" style={{ fontSize: '2rem' }}></i>
              </div>
              <h5 className="text-netflix-white">1. Document Processing</h5>
              <p className="text-small">System ingests and processes corporate documents</p>
            </div>
            <div className="col-md-4 text-center">
              <div className="mb-3">
                <i className="fas fa-brain text-netflix-red" style={{ fontSize: '2rem' }}></i>
              </div>
              <h5 className="text-netflix-white">2. AI Analysis</h5>
              <p className="text-small">Advanced AI extracts key business themes</p>
            </div>
            <div className="col-md-4 text-center">
              <div className="mb-3">
                <i className="fas fa-chart-line text-netflix-red" style={{ fontSize: '2rem' }}></i>
              </div>
              <h5 className="text-netflix-white">3. Theme Presentation</h5>
              <p className="text-small">Themes are organized and presented with evidence</p>
            </div>
          </div>
        </div>
      </div>

      {/* Get Started CTA */}
      {!selectedCompany && (
        <div className="text-center mb-5 p-5 netflix-card">
          <h2 className="text-netflix-white mb-3">Get Started</h2>
          <p className="mb-4">Select a company from the dropdown in the navigation bar to begin exploring business themes.</p>
        </div>
      )}
    </div>
  );
};

export default HomePage;
