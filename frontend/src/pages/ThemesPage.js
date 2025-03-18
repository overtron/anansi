import React, { useState, useEffect } from 'react';
import { themesApi } from '../services/api';
import { useCompany } from '../context/CompanyContext';

const ThemesPage = () => {
  const { selectedCompany } = useCompany();
  const [themes, setThemes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');

  useEffect(() => {
    const fetchThemes = async () => {
      if (!selectedCompany) return;
      
      try {
        setLoading(true);
        const data = await themesApi.getAllThemes(selectedCompany.id);
        setThemes(data);
        setLoading(false);
      } catch (err) {
        setError('Failed to fetch themes. Please try again later.');
        setLoading(false);
        console.error('Error fetching themes:', err);
      }
    };

    fetchThemes();
  }, [selectedCompany]);

  // Get unique categories from themes
  const categories = ['All', ...new Set(themes.map(theme => theme.category))];

  // Filter themes based on search term and selected category
  const filteredThemes = themes.filter(theme => {
    const matchesSearch = theme.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
                         theme.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === 'All' || theme.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  // Group themes by category for display
  const groupedThemes = filteredThemes.reduce((acc, theme) => {
    const category = theme.category || 'Uncategorized';
    if (!acc[category]) {
      acc[category] = [];
    }
    acc[category].push(theme);
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
    <div className="themes-page">
      <h1 className="mb-4">{selectedCompany ? `${selectedCompany.name} Business Themes` : 'Business Themes'}</h1>
      
      <div className="row mb-4">
        <div className="col-md-6">
          <div className="input-group">
            <input
              type="text"
              className="form-control"
              placeholder="Search themes..."
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
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
          >
            {categories.map(category => (
              <option key={category} value={category}>
                {category}
              </option>
            ))}
          </select>
        </div>
      </div>

      {Object.keys(groupedThemes).length === 0 ? (
        <div className="alert alert-info">
          No themes found matching your search criteria.
        </div>
      ) : (
        Object.entries(groupedThemes).map(([category, categoryThemes]) => (
          <div key={category}>
            <h2 className="theme-category">{category}</h2>
            <div className="row">
              {categoryThemes.map(theme => (
                <div key={theme.name} className="col-md-6 mb-4">
                  <div className="card theme-card">
                    <div className="card-header">
                      {theme.name}
                    </div>
                    <div className="card-body">
                      <p className="card-text">{theme.description}</p>
                      {theme.evidence && (
                        <div>
                          <h6 className="card-subtitle mb-2 text-muted">Evidence:</h6>
                          <p className="card-text">{theme.evidence}</p>
                        </div>
                      )}
                      {theme.source && (
                        <div className="mt-2 text-muted small">
                          <strong>Source:</strong> {theme.source}
                        </div>
                      )}
                      {!theme.source && (
                        <div className="mt-2 text-muted small">
                          <em>Manually added theme</em>
                        </div>
                      )}
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

export default ThemesPage;
