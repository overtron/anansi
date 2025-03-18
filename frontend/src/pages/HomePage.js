import React from 'react';
import { Link } from 'react-router-dom';
import { useCompany } from '../context/CompanyContext';

const HomePage = () => {
  const { selectedCompany } = useCompany();
  return (
    <div className="home-page">
      <div className="jumbotron bg-light p-5 rounded mb-4">
        <h1 className="display-4">Company Theme Extraction System</h1>
        <p className="lead">
          Explore business growth and contraction themes extracted from {selectedCompany ? `${selectedCompany.name}'s` : 'company'} investor relations documents and SEC filings.
        </p>
        <hr className="my-4" />
        <p>
          This system uses advanced AI to identify key business themes and allows you to ask questions about them.
        </p>
        <div className="d-flex gap-2 mt-4">
          <Link to="/themes" className="btn btn-danger">View Themes</Link>
          <Link to="/questions" className="btn btn-outline-danger">Ask Questions</Link>
        </div>
      </div>

      <div className="row mt-5">
        <div className="col-md-4">
          <div className="card h-100">
            <div className="card-body">
              <h5 className="card-title">Theme Exploration</h5>
              <p className="card-text">
                Browse through extracted business themes organized by category. Each theme includes supporting evidence from source documents.
              </p>
              <Link to="/themes" className="btn btn-sm btn-outline-danger">Explore Themes</Link>
            </div>
          </div>
        </div>
        <div className="col-md-4">
          <div className="card h-100">
            <div className="card-body">
              <h5 className="card-title">Question Answering</h5>
              <p className="card-text">
                Ask questions about {selectedCompany ? `${selectedCompany.name}'s` : 'company'} business themes and get AI-powered answers with citations from source documents.
              </p>
              <Link to="/questions" className="btn btn-sm btn-outline-danger">Ask Questions</Link>
            </div>
          </div>
        </div>
        <div className="col-md-4">
          <div className="card h-100">
            <div className="card-body">
              <h5 className="card-title">Document Management</h5>
              <p className="card-text">
                View the source documents used for theme extraction, including investor relations PDFs and SEC filings.
              </p>
              <Link to="/documents" className="btn btn-sm btn-outline-danger">View Documents</Link>
            </div>
          </div>
        </div>
      </div>

      <div className="mt-5 p-4 bg-light rounded">
        <h3>How It Works</h3>
        <p>
          This system uses OpenAI's GPT-4o model to analyze {selectedCompany ? `${selectedCompany.name}'s` : 'company'} investor relations documents and SEC filings, 
          extracting key business themes related to growth and contraction factors. The themes are categorized and 
          presented with supporting evidence from the source documents.
        </p>
        <p>
          You can also ask questions about the themes, and the system will provide answers based on the source documents,
          with proper citations to help you understand the context.
        </p>
      </div>
    </div>
  );
};

export default HomePage;
