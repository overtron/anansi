import React, { useState, useEffect } from 'react';
import { questionsApi } from '../services/api';
import { useCompany } from '../context/CompanyContext';

const QuestionsPage = () => {
  const { selectedCompany } = useCompany();
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [queryHistory, setQueryHistory] = useState([]);
  const [showExamples, setShowExamples] = useState(true);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!question.trim()) {
      setError('Please enter a question');
      return;
    }

    if (!selectedCompany) {
      setError('Please select a company first');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      setAnswer(null);
      
      // Add to query history
      const newQuery = {
        text: question,
        timestamp: new Date().toISOString()
      };
      setQueryHistory(prev => [newQuery, ...prev]);
      
      const response = await questionsApi.askQuestion(question, selectedCompany.id);
      setAnswer(response);
      setLoading(false);
      setShowExamples(false);
    } catch (err) {
      setError('Failed to get an answer. Please try again later.');
      setLoading(false);
      console.error('Error asking question:', err);
    }
  };

  // Example questions to help users get started
  const getExampleQuestions = () => {
    if (!selectedCompany) return [];
    
    const companyName = selectedCompany.name;
    return [
      `Why isn't 'international licensing' listed as a theme for ${companyName}?`,
      `Is there evidence for 'content localization' as a growth strategy for ${companyName}?`,
      `What does the data say about ${companyName}'s approach to original content?`,
      `How does ${companyName} view competition from other streaming services?`,
      `What are the main financial growth drivers mentioned in the ${companyName} documents?`
    ];
  };
  
  const exampleQuestions = getExampleQuestions();

  const handleExampleClick = (exampleQuestion) => {
    setQuestion(exampleQuestion);
  };

  // Format the timestamp for display
  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit',
      hour12: false 
    });
  };

  return (
    <div className="questions-page netflix-fade-in">
      <h1 className="mb-4">Ask Questions About {selectedCompany ? selectedCompany.name : ''} Themes</h1>
      
      <div className="row">
        <div className="col-lg-8">
          {/* Main Query Panel */}
          <div className="netflix-panel mb-4">
            <div className="netflix-panel-header">
              <span>Ask a Question</span>
            </div>
            <div className="netflix-panel-body">
              <form onSubmit={handleSubmit}>
                <div className="netflix-query-input mb-3">
                  <input
                    type="text"
                    className="netflix-form-control"
                    placeholder="e.g., What are the main growth drivers?"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    disabled={loading}
                  />
                  <button 
                    type="submit" 
                    className="netflix-btn"
                    disabled={loading || !question.trim()}
                  >
                    {loading ? 'Processing...' : 'Ask'}
                  </button>
                </div>
              </form>
              
              {error && (
                <div className="netflix-alert netflix-alert-danger mt-3">
                  {error}
                </div>
              )}
              
              {loading && (
                <div className="netflix-loading mt-4">
                  <div className="netflix-spinner"></div>
                  <p className="mt-3">Analyzing documents and generating answer...</p>
                </div>
              )}
            </div>
          </div>
          
          {/* Answer Display */}
          {answer && (
            <div className="netflix-panel mb-4 netflix-slide-up">
              <div className="netflix-panel-header">
                <span>Answer</span>
                <span className="text-netflix-success">Found</span>
              </div>
              <div className="netflix-panel-body">
                <div className="mb-3">
                  <h5 className="text-netflix-white mb-2">Question</h5>
                  <p>{answer.question}</p>
                </div>
                <div className="mb-4">
                  <h5 className="text-netflix-white mb-2">Answer</h5>
                  <div style={{ whiteSpace: 'pre-line' }}>{answer.answer}</div>
                </div>
                {answer.sources && answer.sources.length > 0 && (
                  <div>
                    <h5 className="text-netflix-white mb-2">Sources</h5>
                    <ul className="list-unstyled">
                      {answer.sources.map((source, index) => (
                        <li key={index} className="text-small mb-1">{source}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
        
        <div className="col-lg-4">
          {/* Query History */}
          <div className="netflix-panel mb-4">
            <div className="netflix-panel-header">
              <span>Recent Queries</span>
              {queryHistory.length > 0 && (
                <button 
                  className="netflix-btn netflix-btn-sm"
                  onClick={() => setQueryHistory([])}
                >
                  Clear
                </button>
              )}
            </div>
            <div className="netflix-panel-body" style={{ maxHeight: '300px', overflowY: 'auto' }}>
              {queryHistory.length === 0 ? (
                <p className="text-small">No queries yet. Ask a question to get started.</p>
              ) : (
                <ul className="list-unstyled">
                  {queryHistory.map((item, index) => (
                    <li 
                      key={index} 
                      className="mb-2 p-2 border-bottom"
                      style={{ cursor: 'pointer' }}
                      onClick={() => setQuestion(item.text)}
                    >
                      <div className="d-flex justify-content-between">
                        <span className="text-netflix-white">{item.text}</span>
                        <span className="text-small">{formatTimestamp(item.timestamp)}</span>
                      </div>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>
          
          {/* Example Questions */}
          {showExamples && (
            <div className="netflix-panel">
              <div className="netflix-panel-header">
                <span>Example Questions</span>
              </div>
              <div className="netflix-panel-body">
                <p className="text-small mb-3">Click on any example to use it:</p>
                <ul className="list-unstyled">
                  {exampleQuestions.map((exampleQuestion, index) => (
                    <li 
                      key={index} 
                      className="mb-2 p-2 border-bottom"
                      style={{ cursor: 'pointer' }}
                      onClick={() => handleExampleClick(exampleQuestion)}
                    >
                      {exampleQuestion}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </div>
      </div>
      
      {/* How to Ask Section */}
      <div className="netflix-panel mt-4">
        <div className="netflix-panel-header">
          <span>How to Ask Effective Questions</span>
        </div>
        <div className="netflix-panel-body">
          <div className="row">
            <div className="col-md-4 mb-3">
              <h5 className="text-netflix-white">Be Specific</h5>
              <p className="text-small">
                Ask about specific themes, time periods, or business aspects for more precise answers.
              </p>
            </div>
            <div className="col-md-4 mb-3">
              <h5 className="text-netflix-white">Use Context</h5>
              <p className="text-small">
                Mention specific documents or sources if you're looking for information from particular materials.
              </p>
            </div>
            <div className="col-md-4 mb-3">
              <h5 className="text-netflix-white">Ask Comparisons</h5>
              <p className="text-small">
                Compare themes, quarters, or strategies to get insights about changes and trends.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default QuestionsPage;
