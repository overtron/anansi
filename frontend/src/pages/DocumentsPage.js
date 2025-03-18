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
  const [sortConfig, setSortConfig] = useState({ key: 'path', direction: 'ascending' });
  const [viewMode, setViewMode] = useState('grid'); // 'grid' or 'table'
  const [selectedDocument, setSelectedDocument] = useState(null);

  useEffect(() => {
    const fetchDocuments = async () => {
      if (!selectedCompany) return;
      
      try {
        setLoading(true);
        const data = await documentsApi.getDocumentsByCompany(selectedCompany.id);
        
        // Process documents to extract more metadata
        const processedDocs = data.map(doc => {
          // Extract document type from path
          const fileExtension = doc.path.split('.').pop().toLowerCase();
          const docType = fileExtension === 'pdf' ? 'PDF' : 
                         fileExtension === 'json' ? 'JSON' : 
                         fileExtension === 'txt' ? 'TEXT' : 'Other';
          
          // Extract date from filename if possible
          const dateMatch = doc.path.match(/(\d{4}[-_]\d{1,2}[-_]\d{1,2})|(\d{1,2}[-_]\d{1,2}[-_]\d{4})/);
          const docDate = dateMatch ? dateMatch[0].replace(/_/g, '-') : 'Unknown';
          
          // Extract document category from path
          let category = 'Other';
          if (doc.path.toLowerCase().includes('shareholder')) category = 'Shareholder';
          else if (doc.path.toLowerCase().includes('earnings')) category = 'Earnings';
          else if (doc.path.toLowerCase().includes('conference')) category = 'Conference';
          else if (doc.path.toLowerCase().includes('sec')) category = 'SEC Filing';
          
          return {
            ...doc,
            type: docType,
            date: docDate,
            category: category,
            size: Math.floor(Math.random() * 5000) + 100 + 'KB', // Mock file size
            pages: docType === 'PDF' ? Math.floor(Math.random() * 50) + 5 : 'N/A' // Mock page count for PDFs
          };
        });
        
        setDocuments(processedDocs);
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
    const matchesSearch = doc.path.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesType = selectedType === 'All' || doc.type === selectedType;
    return matchesSearch && matchesType;
  });

  // Sort documents based on current sort configuration
  const sortedDocuments = [...filteredDocuments].sort((a, b) => {
    if (a[sortConfig.key] < b[sortConfig.key]) {
      return sortConfig.direction === 'ascending' ? -1 : 1;
    }
    if (a[sortConfig.key] > b[sortConfig.key]) {
      return sortConfig.direction === 'ascending' ? 1 : -1;
    }
    return 0;
  });

  // Request a sort
  const requestSort = (key) => {
    let direction = 'ascending';
    if (sortConfig.key === key && sortConfig.direction === 'ascending') {
      direction = 'descending';
    }
    setSortConfig({ key, direction });
  };

  // Get sort indicator
  const getSortIndicator = (key) => {
    if (sortConfig.key !== key) return '';
    return sortConfig.direction === 'ascending' ? ' ▲' : ' ▼';
  };

  // View document details
  const viewDocumentDetails = (document) => {
    setSelectedDocument(document);
  };

  // Back to document list
  const backToDocuments = () => {
    setSelectedDocument(null);
  };

  // Get document icon based on type
  const getDocumentIcon = (type) => {
    switch (type) {
      case 'PDF':
        return '📄';
      case 'JSON':
        return '📋';
      case 'TEXT':
        return '📝';
      default:
        return '📁';
    }
  };

  // Group documents by category
  const documentsByCategory = sortedDocuments.reduce((acc, doc) => {
    if (!acc[doc.category]) {
      acc[doc.category] = [];
    }
    acc[doc.category].push(doc);
    return acc;
  }, {});

  if (loading) {
    return (
      <div className="netflix-loading">
        <div className="netflix-spinner"></div>
        <p className="mt-3">Loading documents...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="netflix-alert netflix-alert-danger">
        {error}
      </div>
    );
  }

  // Document detail view
  if (selectedDocument) {
    return (
      <div className="documents-page netflix-fade-in">
        <div className="d-flex justify-content-between align-items-center mb-4">
          <h1>{selectedDocument.path.split('/').pop()}</h1>
          <button className="netflix-btn netflix-btn-secondary" onClick={backToDocuments}>
            Back to Documents
          </button>
        </div>
        
        <div className="netflix-panel">
          <div className="netflix-panel-header">
            <span>Document Details</span>
            <span className="text-netflix-white">{selectedDocument.type}</span>
          </div>
          <div className="netflix-panel-body">
            <div className="row">
              <div className="col-md-8">
                <table className="w-100">
                  <tbody>
                    <tr>
                      <td className="text-netflix-white" style={{ width: '150px', padding: '8px 0' }}>Path:</td>
                      <td>{selectedDocument.path}</td>
                    </tr>
                    <tr>
                      <td className="text-netflix-white" style={{ padding: '8px 0' }}>Category:</td>
                      <td>{selectedDocument.category}</td>
                    </tr>
                    <tr>
                      <td className="text-netflix-white" style={{ padding: '8px 0' }}>Date:</td>
                      <td>{selectedDocument.date}</td>
                    </tr>
                    <tr>
                      <td className="text-netflix-white" style={{ padding: '8px 0' }}>Size:</td>
                      <td>{selectedDocument.size}</td>
                    </tr>
                    {selectedDocument.type === 'PDF' && (
                      <tr>
                        <td className="text-netflix-white" style={{ padding: '8px 0' }}>Pages:</td>
                        <td>{selectedDocument.pages}</td>
                      </tr>
                    )}
                    <tr>
                      <td className="text-netflix-white" style={{ padding: '8px 0' }}>Company:</td>
                      <td>{selectedCompany?.name}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div className="col-md-4 text-center">
                <div style={{ fontSize: '4rem', marginBottom: '1rem' }}>
                  {getDocumentIcon(selectedDocument.type)}
                </div>
                <div className="text-netflix-white">{selectedDocument.type} Document</div>
              </div>
            </div>
            
            <div className="mt-4 text-center">
              <div className="text-netflix-white mb-2">Document Preview Not Available</div>
              <p className="text-small">
                This is a document reference system. To view the actual document content, please access the original file.
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="documents-page netflix-fade-in">
      <h1 className="mb-4">{selectedCompany ? `${selectedCompany.name} Documents` : 'Documents'}</h1>
      
      {/* Search and Filter Controls */}
      <div className="netflix-panel mb-4">
        <div className="netflix-panel-header">
          <span>Search & Filter</span>
          <span>{filteredDocuments.length} documents found</span>
        </div>
        <div className="netflix-panel-body">
          <div className="row">
            <div className="col-md-8 mb-3 mb-md-0">
              <input
                type="text"
                className="netflix-form-control"
                placeholder="Search documents..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
            <div className="col-md-4">
              <select
                className="netflix-form-select"
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
        </div>
      </div>

      {/* View Toggle */}
      <div className="d-flex justify-content-end mb-4">
        <div className="btn-group">
          <button 
            className={`netflix-btn netflix-btn-sm ${viewMode === 'grid' ? '' : 'netflix-btn-secondary'}`}
            onClick={() => setViewMode('grid')}
          >
            Grid View
          </button>
          <button 
            className={`netflix-btn netflix-btn-sm ${viewMode === 'table' ? '' : 'netflix-btn-secondary'}`}
            onClick={() => setViewMode('table')}
          >
            Table View
          </button>
        </div>
      </div>

      {filteredDocuments.length === 0 ? (
        <div className="netflix-alert netflix-alert-info">
          No documents found matching your search criteria.
        </div>
      ) : viewMode === 'table' ? (
        // Table View
        <div className="netflix-panel">
          <div className="netflix-panel-header">
            <span>Documents Table</span>
          </div>
          <div className="netflix-panel-body p-0">
            <table className="netflix-table">
              <thead>
                <tr>
                  <th onClick={() => requestSort('path')} style={{cursor: 'pointer'}}>
                    Filename {getSortIndicator('path')}
                  </th>
                  <th onClick={() => requestSort('type')} style={{cursor: 'pointer'}}>
                    Type {getSortIndicator('type')}
                  </th>
                  <th onClick={() => requestSort('category')} style={{cursor: 'pointer'}}>
                    Category {getSortIndicator('category')}
                  </th>
                  <th onClick={() => requestSort('date')} style={{cursor: 'pointer'}}>
                    Date {getSortIndicator('date')}
                  </th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {sortedDocuments.map((doc, index) => (
                  <tr key={index}>
                    <td>{doc.path.split('/').pop()}</td>
                    <td>{doc.type}</td>
                    <td>{doc.category}</td>
                    <td>{doc.date}</td>
                    <td>
                      <button 
                        className="netflix-btn netflix-btn-sm"
                        onClick={() => viewDocumentDetails(doc)}
                      >
                        View Details
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ) : (
        // Grid View - Grouped by Category
        Object.entries(documentsByCategory).map(([category, categoryDocs]) => (
          <div key={category} className="netflix-row mb-5">
            <h2 className="netflix-row-title">{category}</h2>
            <div className="netflix-document-grid">
              {categoryDocs.map((doc, index) => (
                <div 
                  key={index} 
                  className="netflix-card netflix-document-card"
                  onClick={() => viewDocumentDetails(doc)}
                  style={{cursor: 'pointer'}}
                >
                  <div className="text-center">
                    <div className="netflix-document-icon">
                      {getDocumentIcon(doc.type)}
                    </div>
                    <div className="text-netflix-white">
                      {doc.path.split('/').pop().length > 20 
                        ? `${doc.path.split('/').pop().substring(0, 20)}...` 
                        : doc.path.split('/').pop()}
                    </div>
                  </div>
                  <div className="netflix-document-info">
                    <div className="netflix-document-title">{doc.path.split('/').pop()}</div>
                    <div className="netflix-document-meta">
                      {doc.type} • {doc.date} • {doc.size}
                    </div>
                  </div>
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
