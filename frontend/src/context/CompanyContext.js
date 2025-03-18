import React, { createContext, useState, useContext, useEffect } from 'react';
import { companiesApi } from '../services/api';

// Create context
const CompanyContext = createContext();

// Create provider component
export const CompanyProvider = ({ children }) => {
  const [companies, setCompanies] = useState([]);
  const [selectedCompany, setSelectedCompany] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch companies on mount
  useEffect(() => {
    const fetchCompanies = async () => {
      try {
        setLoading(true);
        const data = await companiesApi.getAllCompanies();
        setCompanies(data);
        
        // Set default selected company to the first one
        if (data.length > 0 && !selectedCompany) {
          setSelectedCompany(data[0]);
        }
        
        setLoading(false);
      } catch (err) {
        console.error('Error fetching companies:', err);
        setError('Failed to load companies. Please try again later.');
        setLoading(false);
      }
    };

    fetchCompanies();
  }, []);

  // Change selected company
  const changeCompany = (companyId) => {
    const company = companies.find(c => c.id === companyId);
    if (company) {
      setSelectedCompany(company);
    }
  };

  return (
    <CompanyContext.Provider
      value={{
        companies,
        selectedCompany,
        changeCompany,
        loading,
        error
      }}
    >
      {children}
    </CompanyContext.Provider>
  );
};

// Custom hook to use the company context
export const useCompany = () => {
  const context = useContext(CompanyContext);
  if (!context) {
    throw new Error('useCompany must be used within a CompanyProvider');
  }
  return context;
};

export default CompanyContext;
