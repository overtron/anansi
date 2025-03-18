import axios from 'axios';

// Create an axios instance with default config
const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Theme API endpoints
export const themesApi = {
  // Get all themes
  getAllThemes: async () => {
    try {
      const response = await api.get('/themes');
      return response.data;
    } catch (error) {
      console.error('Error fetching themes:', error);
      throw error;
    }
  },

  // Get a theme by name
  getThemeByName: async (name) => {
    try {
      const response = await api.get(`/themes/${name}`);
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
  deleteTheme: async (name) => {
    try {
      const response = await api.delete(`/themes/${name}`);
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
  askQuestion: async (question) => {
    try {
      const response = await api.post('/questions/ask', { question });
      return response.data;
    } catch (error) {
      console.error('Error asking question:', error);
      throw error;
    }
  },
};

// Document API endpoints
export const documentsApi = {
  // Get all documents
  getAllDocuments: async () => {
    try {
      const response = await api.get('/documents');
      return response.data;
    } catch (error) {
      console.error('Error fetching documents:', error);
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
  themes: themesApi,
  questions: questionsApi,
  documents: documentsApi,
};
