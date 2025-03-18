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
  const [sortConfig, setSortConfig] = useState({ key: 'name', direction: 'ascending' });
  const [viewMode, setViewMode] = useState('grid'); // 'grid' or 'detail'
  const [selectedTheme, setSelectedTheme] = useState(null);

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

  // Sort themes based on current sort configuration
  const sortedThemes = [...filteredThemes].sort((a, b) => {
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

  // Determine theme trend (for color coding)
  const getThemeTrend = (theme) => {
    const lowerDesc = theme.description.toLowerCase();
    if (lowerDesc.includes('growth') || lowerDesc.includes('increase') || lowerDesc.includes('expanding')) {
      return 'positive';
    } else if (lowerDesc.includes('decline') || lowerDesc.includes('decrease') || lowerDesc.includes('contracting')) {
      return 'negative';
    }
    return 'neutral';
  };

  // View theme details
  const viewThemeDetails = (theme) => {
    setSelectedTheme(theme);
    setViewMode('detail');
  };

  // Back to grid view
  const backToGrid = () => {
    setViewMode('grid');
    setSelectedTheme(null);
  };

  // Group themes by category for grid view
  const groupedThemes = sortedThemes.reduce((acc, theme) => {
    const category = theme.category || 'Uncategorized';
    if (!acc[category]) {
      acc[category] = [];
    }
    acc[category].push(theme);
    return acc;
  }, {});

  if (loading) {
    return (
      <div className="netflix-loading">
        <div className="netflix-spinner"></div>
        <p className="mt-3">Loading themes...</p>
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

  // Detail view for a single theme
  if (viewMode === 'detail' && selectedTheme) {
    return (
      <div className="themes-page netflix-fade-in">
        <div className="d-flex justify-content-between align-items-center mb-4">
          <h1>{selectedTheme.name}</h1>
          <button className="netflix-btn netflix-btn-secondary" onClick={backToGrid}>
            Back to Themes
          </button>
        </div>
        
        <div className="netflix-panel">
          <div className="netflix-panel-header">
            <span>Theme Details</span>
            <span className={`text-${getThemeTrend(selectedTheme) === 'positive' ? 'netflix-success' : getThemeTrend(selectedTheme) === 'negative' ? 'netflix-error' : 'netflix-warning'}`}>
              {selectedTheme.category || 'Uncategorized'}
            </span>
          </div>
          <div className="netflix-panel-body">
            <div className="mb-4">
              <h5 className="text-netflix-white mb-2">Description</h5>
              <p>{selectedTheme.description}</p>
            </div>
            
            {selectedTheme.evidence && (
              <div className="mb-4">
                <h5 className="text-netflix-white mb-2">Evidence</h5>
                <p>{selectedTheme.evidence}</p>
              </div>
            )}
            
            <div>
              <h5 className="text-netflix-white mb-2">Source</h5>
              <p className="text-small">
                {selectedTheme.source || 'Manually added theme'}
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Grid view (default)
  return (
    <div className="themes-page netflix-fade-in">
      <h1 className="mb-4">{selectedCompany ? `${selectedCompany.name} Business Themes` : 'Business Themes'}</h1>
      
      {/* Search and Filter Controls */}
      <div className="netflix-panel mb-4">
        <div className="netflix-panel-header">
          <span>Search & Filter</span>
          <span>{filteredThemes.length} themes found</span>
        </div>
        <div className="netflix-panel-body">
          <div className="row">
            <div className="col-md-8 mb-3 mb-md-0">
              <input
                type="text"
                className="netflix-form-control"
                placeholder="Search themes..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
            <div className="col-md-4">
              <select
                className="netflix-form-select"
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

      {filteredThemes.length === 0 ? (
        <div className="netflix-alert netflix-alert-info">
          No themes found matching your search criteria.
        </div>
      ) : viewMode === 'table' ? (
        // Table View
        <div className="netflix-panel">
          <div className="netflix-panel-header">
            <span>Themes Table</span>
          </div>
          <div className="netflix-panel-body p-0">
            <table className="netflix-table">
              <thead>
                <tr>
                  <th onClick={() => requestSort('name')} style={{cursor: 'pointer'}}>
                    Name {getSortIndicator('name')}
                  </th>
                  <th onClick={() => requestSort('category')} style={{cursor: 'pointer'}}>
                    Category {getSortIndicator('category')}
                  </th>
                  <th>Description</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {sortedThemes.map(theme => (
                  <tr key={theme.name}>
                    <td>{theme.name}</td>
                    <td>{theme.category || 'Uncategorized'}</td>
                    <td>
                      {theme.description.length > 100 
                        ? `${theme.description.substring(0, 100)}...` 
                        : theme.description}
                    </td>
                    <td>
                      <button 
                        className="netflix-btn netflix-btn-sm"
                        onClick={() => viewThemeDetails(theme)}
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
        Object.entries(groupedThemes).map(([category, categoryThemes]) => (
          <div key={category} className="netflix-row mb-5">
            <h2 className="netflix-row-title">{category}</h2>
            <div className="netflix-row-content">
              {categoryThemes.map(theme => (
                <div key={theme.name} className="netflix-row-item">
                  <div 
                    className="netflix-card" 
                    onClick={() => viewThemeDetails(theme)}
                    style={{cursor: 'pointer'}}
                  >
                    <div className="netflix-card-header">
                      {theme.name}
                    </div>
                    <div className="netflix-card-body">
                      <p className="mb-3">
                        {theme.description.length > 120 
                          ? `${theme.description.substring(0, 120)}...` 
                          : theme.description}
                      </p>
                      {theme.source && (
                        <div className="text-small text-netflix-white mt-2">
                          Source: {theme.source}
                        </div>
                      )}
                      {!theme.source && (
                        <div className="text-small text-netflix-white mt-2">
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
