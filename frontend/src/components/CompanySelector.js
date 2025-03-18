import React from 'react';
import { useCompany } from '../context/CompanyContext';

const CompanySelector = () => {
  const { companies, selectedCompany, changeCompany, loading, error } = useCompany();

  if (loading) {
    return <div>Loading companies...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  if (!companies || companies.length === 0) {
    return <div>No companies available</div>;
  }

  return (
    <div className="company-selector">
      <label htmlFor="company-select">Select Company: </label>
      <select
        id="company-select"
        value={selectedCompany?.id || ''}
        onChange={(e) => changeCompany(e.target.value)}
      >
        {companies.map((company) => (
          <option key={company.id} value={company.id}>
            {company.name}
          </option>
        ))}
      </select>
    </div>
  );
};

export default CompanySelector;
