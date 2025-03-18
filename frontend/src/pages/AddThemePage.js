import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { themesApi } from '../services/api';
import { useCompany } from '../context/CompanyContext';

const AddThemePage = () => {
  const { selectedCompany } = useCompany();
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    category: '',
    evidence: '',
  });
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!selectedCompany) {
      setError('Please select a company first');
      return;
    }
    
    if (!formData.name || !formData.description) {
      setError('Name and description are required');
      return;
    }
    
    try {
      setLoading(true);
      setError(null);
      
      const themeData = {
        ...formData,
        company_id: selectedCompany.id
      };
      
      await themesApi.createTheme(themeData);
      
      setSuccess(true);
      setLoading(false);
      
      // Reset form after successful submission
      setFormData({
        name: '',
        description: '',
        category: '',
        evidence: '',
      });
      
      // Redirect to themes page after 2 seconds
      setTimeout(() => {
        navigate('/themes');
      }, 2000);
      
    } catch (err) {
      setError('Failed to create theme. Please try again later.');
      setLoading(false);
      console.error('Error creating theme:', err);
    }
  };
  
  const handleReset = () => {
    setFormData({
      name: '',
      description: '',
      category: '',
      evidence: '',
    });
    setError(null);
    setSuccess(false);
  };
  
  // Predefined categories
  const categories = [
    'Growth',
    'Revenue',
    'Content',
    'Technology',
    'Strategy',
    'Competition',
    'Market',
    'Regulation',
    'Financial',
    'Operations',
    'International',
    'Diversification'
  ];

  return (
    <div className="add-theme-page netflix-fade-in">
      <h1 className="mb-4">Add New Theme</h1>
      
      <div className="row">
        <div className="col-lg-8">
          <div className="netflix-panel mb-4">
            <div className="netflix-panel-header">
              <span>Theme Information</span>
              {success && <span className="text-netflix-success">Theme Added Successfully</span>}
            </div>
            <div className="netflix-panel-body">
              {!selectedCompany ? (
                <div className="netflix-alert netflix-alert-danger">
                  Please select a company from the dropdown in the navigation bar before adding a theme.
                </div>
              ) : (
                <form onSubmit={handleSubmit}>
                  <div className="netflix-form-group">
                    <label className="netflix-form-label">Theme Name</label>
                    <input
                      type="text"
                      name="name"
                      className="netflix-form-control"
                      value={formData.name}
                      onChange={handleChange}
                      placeholder="e.g., Content Investment Strategy"
                      disabled={loading || success}
                    />
                    <div className="text-small mt-1">
                      Enter a concise name that captures the essence of the theme
                    </div>
                  </div>
                  
                  <div className="netflix-form-group">
                    <label className="netflix-form-label">Category</label>
                    <select
                      name="category"
                      className="netflix-form-select"
                      value={formData.category}
                      onChange={handleChange}
                      disabled={loading || success}
                    >
                      <option value="">Select a category</option>
                      {categories.map(category => (
                        <option key={category} value={category}>
                          {category}
                        </option>
                      ))}
                    </select>
                    <div className="text-small mt-1">
                      Categorize the theme to help with organization and filtering
                    </div>
                  </div>
                  
                  <div className="netflix-form-group">
                    <label className="netflix-form-label">Description</label>
                    <textarea
                      name="description"
                      className="netflix-form-control"
                      rows="4"
                      value={formData.description}
                      onChange={handleChange}
                      placeholder="Describe the theme and its significance to the company's business..."
                      disabled={loading || success}
                    ></textarea>
                    <div className="text-small mt-1">
                      Provide a detailed explanation of what this theme represents and why it's important
                    </div>
                  </div>
                  
                  <div className="netflix-form-group">
                    <label className="netflix-form-label">Supporting Evidence (Optional)</label>
                    <textarea
                      name="evidence"
                      className="netflix-form-control"
                      rows="4"
                      value={formData.evidence}
                      onChange={handleChange}
                      placeholder="Provide any evidence or quotes from documents that support this theme..."
                      disabled={loading || success}
                    ></textarea>
                    <div className="text-small mt-1">
                      Include specific quotes, data points, or references that support the existence of this theme
                    </div>
                  </div>
                  
                  {error && (
                    <div className="netflix-alert netflix-alert-danger mb-3">
                      {error}
                    </div>
                  )}
                  
                  <div className="d-flex">
                    <button 
                      type="submit" 
                      className="netflix-btn me-2"
                      disabled={loading || success}
                    >
                      {loading ? 'Adding Theme...' : 'Add Theme'}
                    </button>
                    <button 
                      type="button" 
                      className="netflix-btn netflix-btn-secondary"
                      onClick={handleReset}
                      disabled={loading}
                    >
                      Reset Form
                    </button>
                  </div>
                </form>
              )}
              
              {success && (
                <div className="netflix-alert netflix-alert-success mt-3">
                  Theme added successfully! Redirecting to themes page...
                </div>
              )}
            </div>
          </div>
        </div>
        
        <div className="col-lg-4">
          <div className="netflix-panel">
            <div className="netflix-panel-header">
              <span>Guidelines</span>
            </div>
            <div className="netflix-panel-body">
              <h5 className="text-netflix-white mb-3">What Makes a Good Theme?</h5>
              
              <div className="mb-3">
                <h6 className="text-netflix-white">Specificity</h6>
                <p className="text-small">
                  Be specific about the business aspect the theme represents. Avoid overly broad themes.
                </p>
              </div>
              
              <div className="mb-3">
                <h6 className="text-netflix-white">Evidence-Based</h6>
                <p className="text-small">
                  Themes should be supported by evidence from company documents or reliable sources.
                </p>
              </div>
              
              <div className="mb-3">
                <h6 className="text-netflix-white">Business Relevance</h6>
                <p className="text-small">
                  Focus on themes that have a meaningful impact on the company's business strategy or performance.
                </p>
              </div>
              
              <div className="mb-3">
                <h6 className="text-netflix-white">Clear Description</h6>
                <p className="text-small">
                  Write descriptions that clearly explain what the theme is and why it matters.
                </p>
              </div>
              
              <div className="mt-4">
                <h6 className="text-netflix-white">Example Theme</h6>
                <div className="netflix-card mt-2">
                  <div className="netflix-card-header">
                    Original Content Investment
                  </div>
                  <div className="netflix-card-body">
                    <p className="text-small">
                      <strong>Category:</strong> Content
                    </p>
                    <p className="text-small">
                      <strong>Description:</strong> Strategic focus on increasing investment in original content production to differentiate from competitors and reduce reliance on licensed content.
                    </p>
                    <p className="text-small">
                      <strong>Evidence:</strong> "We're planning to invest $X billion in original content production this year, up X% from last year."
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AddThemePage;
