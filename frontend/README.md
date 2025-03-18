# Netflix Themes Frontend

This is the frontend for the Netflix Theme Extraction and Question-Answering System. It provides a user-friendly interface for exploring themes extracted from Netflix's investor relations documents and SEC filings, asking questions about the themes, and managing the source documents.

## Features

- **Theme Exploration**: Browse through extracted business themes organized by category
- **Question Answering**: Ask questions about Netflix's business themes and get AI-powered answers
- **Document Management**: View the source documents used for theme extraction
- **Manual Theme Addition**: Add custom themes that will be preserved during updates

## Prerequisites

- Node.js (v14 or higher)
- npm (v6 or higher)
- Backend API running (see the backend README for setup instructions)

## Installation

1. Install dependencies:

```bash
cd filingsdata/frontend
npm install
```

## Development

To run the development server:

```bash
npm start
```

This will start the React development server at [http://localhost:3000](http://localhost:3000). The page will reload if you make edits, and you will see any lint errors in the console.

The development server is configured to proxy API requests to the backend server running at http://localhost:8000.

## Building for Production

To build the app for production:

```bash
npm run build
```

This builds the app for production to the `build` folder. It correctly bundles React in production mode and optimizes the build for the best performance.

## Project Structure

- `public/`: Static files like HTML, icons, etc.
- `src/`: Source code
  - `components/`: Reusable React components
  - `pages/`: Page components for different routes
  - `services/`: API service functions
  - `context/`: React context providers
  - `App.js`: Main application component
  - `index.js`: Entry point

## API Integration

The frontend communicates with the backend API using the service functions defined in `src/services/api.js`. The API endpoints are:

- `/api/themes`: Get, create, update, and delete themes
- `/api/questions/ask`: Ask questions about themes
- `/api/documents`: Get information about source documents

## Deployment

The frontend can be deployed to any static hosting service. Some options include:

- Netlify
- Vercel
- GitHub Pages
- AWS S3 + CloudFront

For a complete solution, you'll need to deploy both the frontend and the backend.
