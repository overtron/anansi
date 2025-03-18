import React from 'react';
import { useCompany } from '../context/CompanyContext';

const CompanySelector = () => {
  const { companies, selectedCompany, changeCompany, loading, error } = useCompany();

  if (loading) {
    return <div className="netflix-loading">Loading...</div>;
  }

  if (error) {
    return <div className="netflix-alert netflix-alert-danger">{error}</div>;
  }

  if (!companies || companies.length === 0) {
    return <div className="text-netflix-white">No companies available</div>;
  }

  return (
    <select
      className="netflix-form-select"
      value={selectedCompany?.id || ''}
      onChange={(e) => changeCompany(e.target.value)}
      aria-label="Select company"
    >
      {companies.map((company) => (
        <option key={company.id} value={company.id}>
          {company.name}
        </option>
      ))}
    </select>
  );
};

export default CompanySelector;
