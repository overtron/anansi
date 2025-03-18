import React, { useState, useEffect } from 'react';
import { documentsApi } from '../services/api';
import { useCompany } from '../context/CompanyContext';

const DocumentsPage = () => {
  const { selectedCompany } = useCompany();
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedType, setSelectedType] = useState('All');

  useEffect(() => {
    const fetchDocuments = async () => {
      if (!selectedCompany) return;
      
      try {
        setLoading(true);
        const data = await documentsApi.getAllDocuments(selectedCompany.id);
        setDocuments(data);
        setLoading(false);
      } catch (err) {
        setError('Failed to fetch documents. Please try again later.');
        setLoading(false);
        console.error('Error fetching documents:', err);
      }
    };

    fetchDocuments();
  }, [selectedCompany]);

  // Get unique document types
  const documentTypes = ['All', ...new Set(documents.map(doc => doc.type))];

  // Filter documents based on search term and selected type
  const filteredDocuments = documents.filter(doc => {
    const matchesSearch = doc.filename.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesType = selectedType === 'All' || doc.type === selectedType;
    return matchesSearch && matchesType;
  });

  // Group documents by type for display
  const groupedDocuments = filteredDocuments.reduce((acc, doc) => {
    const type = doc.type || 'Other';
    if (!acc[type]) {
      acc[type] = [];
    }
    acc[type].push(doc);
    return acc;
  }, {});

  if (loading) {
    return (
      <div className="d-flex justify-content-center mt-5">
        <div className="spinner-border text-danger" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="alert alert-danger" role="alert">
        {error}
      </div>
    );
  }

  return (
    <div className="documents-page">
      <h1 className="mb-4">{selectedCompany ? `${selectedCompany.name} Source Documents` : 'Source Documents'}</h1>
      
      <div className="card mb-4">
        <div className="card-body">
          <h5 className="card-title">About These Documents</h5>
          <p className="card-text">
            These are the source documents used for theme extraction, including investor relations PDFs and SEC filings
            for {selectedCompany ? selectedCompany.name : 'the selected company'}.
            The documents are processed to extract business themes related to growth and contraction factors.
          </p>
        </div>
      </div>
      
      <div className="row mb-4">
        <div className="col-md-6">
          <div className="input-group">
            <input
              type="text"
              className="form-control"
              placeholder="Search documents..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
            {searchTerm && (
              <button
                className="btn btn-outline-secondary"
                type="button"
                onClick={() => setSearchTerm('')}
              >
                Clear
              </button>
            )}
          </div>
        </div>
        <div className="col-md-6">
          <select
            className="form-select"
            value={selectedType}
            onChange={(e) => setSelectedType(e.target.value)}
          >
            {documentTypes.map(type => (
              <option key={type} value={type}>
                {type}
              </option>
            ))}
          </select>
        </div>
      </div>

      {Object.keys(groupedDocuments).length === 0 ? (
        <div className="alert alert-info">
          No documents found matching your search criteria.
        </div>
      ) : (
        Object.entries(groupedDocuments).map(([type, typeDocuments]) => (
          <div key={type} className="mb-5">
            <h2 className="theme-category">{type} Documents</h2>
            <div className="list-group">
              {typeDocuments.map(doc => (
                <div key={doc.path} className="list-group-item list-group-item-action">
                  <div className="d-flex w-100 justify-content-between">
                    <h5 className="mb-1">{doc.filename}</h5>
                    <span className={`badge ${doc.processed ? 'bg-success' : 'bg-secondary'}`}>
                      {doc.processed ? 'Processed' : 'Not Processed'}
                    </span>
                  </div>
                  <p className="mb-1">
                    <small className="text-muted">Path: {doc.path}</small>
                  </p>
                  {doc.processed_date && (
                    <small className="text-muted">
                      Processed on: {new Date(doc.processed_date).toLocaleString()}
                    </small>
                  )}
                </div>
              ))}
            </div>
          </div>
        ))
      )}
    </div>
  );
};

export default DocumentsPage;
