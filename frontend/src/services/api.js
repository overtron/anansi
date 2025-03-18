import axios from 'axios';

// Create an axios instance with default config
const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Company API endpoints
export const companiesApi = {
  // Get all companies
  getAllCompanies: async () => {
    try {
      const response = await api.get('/companies');
      return response.data;
    } catch (error) {
      console.error('Error fetching companies:', error);
      throw error;
    }
  },

  // Get a company by ID
  getCompanyById: async (id) => {
    try {
      const response = await api.get(`/companies/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching company ${id}:`, error);
      throw error;
    }
  },

  // Create a new company
  createCompany: async (company) => {
    try {
      const response = await api.post('/companies', company);
      return response.data;
    } catch (error) {
      console.error('Error creating company:', error);
      throw error;
    }
  },

  // Update a company
  updateCompany: async (id, company) => {
    try {
      const response = await api.put(`/companies/${id}`, company);
      return response.data;
    } catch (error) {
      console.error(`Error updating company ${id}:`, error);
      throw error;
    }
  },

  // Delete a company
  deleteCompany: async (id) => {
    try {
      const response = await api.delete(`/companies/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Error deleting company ${id}:`, error);
      throw error;
    }
  },
};

// Theme API endpoints
export const themesApi = {
  // Get all themes
  getAllThemes: async (companyId) => {
    try {
      const url = companyId ? `/themes?company_id=${companyId}` : '/themes';
      const response = await api.get(url);
      return response.data;
    } catch (error) {
      console.error('Error fetching themes:', error);
      throw error;
    }
  },

  // Get themes for a specific company
  getThemesByCompany: async (companyId) => {
    try {
      const response = await api.get(`/themes/company/${companyId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching themes for company ${companyId}:`, error);
      throw error;
    }
  },

  // Get a theme by name
  getThemeByName: async (name, companyId) => {
    try {
      const url = companyId ? `/themes/${name}?company_id=${companyId}` : `/themes/${name}`;
      const response = await api.get(url);
      return response.data;
    } catch (error) {
      console.error(`Error fetching theme ${name}:`, error);
      throw error;
    }
  },

  // Create a new theme
  createTheme: async (theme) => {
    try {
      const response = await api.post('/themes', theme);
      return response.data;
    } catch (error) {
      console.error('Error creating theme:', error);
      throw error;
    }
  },

  // Update a theme
  updateTheme: async (name, theme) => {
    try {
      const response = await api.put(`/themes/${name}`, theme);
      return response.data;
    } catch (error) {
      console.error(`Error updating theme ${name}:`, error);
      throw error;
    }
  },

  // Delete a theme
  deleteTheme: async (name, companyId) => {
    try {
      const response = await api.delete(`/themes/${name}?company_id=${companyId}`);
      return response.data;
    } catch (error) {
      console.error(`Error deleting theme ${name}:`, error);
      throw error;
    }
  },
};

// Question API endpoints
export const questionsApi = {
  // Ask a question
  askQuestion: async (question, companyId) => {
    try {
      const url = companyId ? `/questions/ask?company_id=${companyId}` : '/questions/ask';
      const response = await api.post(url, { 
        question: question,
        company_id: companyId
      });
      return response.data;
    } catch (error) {
      console.error('Error asking question:', error);
      throw error;
    }
  },

  // Ask a question for a specific company
  askQuestionForCompany: async (companyId, question) => {
    try {
      const response = await api.post(`/questions/company/${companyId}/ask`, { 
        question: question,
        company_id: companyId
      });
      return response.data;
    } catch (error) {
      console.error(`Error asking question for company ${companyId}:`, error);
      throw error;
    }
  },
};

// Document API endpoints
export const documentsApi = {
  // Get all documents
  getAllDocuments: async (companyId) => {
    try {
      const url = companyId ? `/documents?company_id=${companyId}` : '/documents';
      const response = await api.get(url);
      return response.data;
    } catch (error) {
      console.error('Error fetching documents:', error);
      throw error;
    }
  },

  // Get documents for a specific company
  getDocumentsByCompany: async (companyId) => {
    try {
      const response = await api.get(`/documents/company/${companyId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching documents for company ${companyId}:`, error);
      throw error;
    }
  },

  // Get a document by path
  getDocumentByPath: async (path) => {
    try {
      const response = await api.get(`/documents/${path}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching document ${path}:`, error);
      throw error;
    }
  },
};

export default {
  companies: companiesApi,
  themes: themesApi,
  questions: questionsApi,
  documents: documentsApi,
};
