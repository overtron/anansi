import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { themesApi } from '../services/api';

const AddThemePage = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    category: 'General'
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevData => ({
      ...prevData,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate form
    if (!formData.name.trim()) {
      setError('Theme name is required');
      return;
    }
    
    if (!formData.description.trim()) {
      setError('Theme description is required');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      setSuccess(false);
      
      await themesApi.createTheme(formData);
      
      setSuccess(true);
      setLoading(false);
      
      // Reset form
      setFormData({
        name: '',
        description: '',
        category: 'General'
      });
      
      // Redirect to themes page after a short delay
      setTimeout(() => {
        navigate('/themes');
      }, 2000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create theme. Please try again.');
      setLoading(false);
      console.error('Error creating theme:', err);
    }
  };

  // Common categories for themes
  const categories = [
    'General',
    'Content Strategy',
    'Technology',
    'Financial Performance',
    'Market Expansion',
    'Competition',
    'Subscriber Growth',
    'Regulatory',
    'Strategic Initiatives',
    'Other'
  ];

  return (
    <div className="add-theme-page">
      <h1 className="mb-4">Add Manual Theme</h1>
      
      <div className="card mb-4">
        <div className="card-body">
          <h5 className="card-title">About Manual Themes</h5>
          <p className="card-text">
            Manual themes are preserved during updates and can be used to add themes that might not be automatically extracted.
            These themes will be marked as "Manually added" in the themes list.
          </p>
        </div>
      </div>

      {success && (
        <div className="alert alert-success" role="alert">
          Theme created successfully! Redirecting to themes page...
        </div>
      )}

      {error && (
        <div className="alert alert-danger" role="alert">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label htmlFor="name" className="form-label">Theme Name</label>
          <input
            type="text"
            className="form-control"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            placeholder="e.g., Content Localization Strategy"
            maxLength={100}
          />
          <div className="form-text">A concise name (1-5 words) for the theme</div>
        </div>
        
        <div className="mb-3">
          <label htmlFor="description" className="form-label">Description</label>
          <textarea
            className="form-control"
            id="description"
            name="description"
            rows="4"
            value={formData.description}
            onChange={handleChange}
            placeholder="Describe how this theme relates to Netflix's business growth or contraction..."
          ></textarea>
          <div className="form-text">A brief description explaining how this theme impacts Netflix's business</div>
        </div>
        
        <div className="mb-3">
          <label htmlFor="category" className="form-label">Category</label>
          <select
            className="form-select"
            id="category"
            name="category"
            value={formData.category}
            onChange={handleChange}
          >
            {categories.map(category => (
              <option key={category} value={category}>
                {category}
              </option>
            ))}
          </select>
          <div className="form-text">The category this theme belongs to</div>
        </div>
        
        <div className="d-flex gap-2">
          <button type="submit" className="btn btn-danger" disabled={loading}>
            {loading ? (
              <>
                <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                Creating...
              </>
            ) : (
              'Create Theme'
            )}
          </button>
          <button
            type="button"
            className="btn btn-outline-secondary"
            onClick={() => navigate('/themes')}
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

export default AddThemePage;
