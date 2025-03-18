import React, { useState } from 'react';
import { questionsApi } from '../services/api';

const QuestionsPage = () => {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!question.trim()) {
      setError('Please enter a question');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      setAnswer(null);
      
      const response = await questionsApi.askQuestion(question);
      setAnswer(response);
      setLoading(false);
    } catch (err) {
      setError('Failed to get an answer. Please try again later.');
      setLoading(false);
      console.error('Error asking question:', err);
    }
  };

  // Example questions to help users get started
  const exampleQuestions = [
    "Why isn't 'international licensing' listed as a theme?",
    "Is there evidence for 'content localization' as a growth strategy?",
    "What does the data say about Netflix's approach to original content?",
    "How does Netflix view competition from other streaming services?",
    "What are the main financial growth drivers mentioned in the documents?"
  ];

  const handleExampleClick = (exampleQuestion) => {
    setQuestion(exampleQuestion);
  };

  return (
    <div className="questions-page">
      <h1 className="mb-4">Ask Questions About Themes</h1>
      
      <div className="card mb-4">
        <div className="card-body">
          <h5 className="card-title">How It Works</h5>
          <p className="card-text">
            Ask questions about Netflix's business themes and get AI-powered answers with citations from source documents.
            You can ask about existing themes, missing themes, or any other aspect of Netflix's business strategy.
          </p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="question-form">
        <div className="mb-3">
          <label htmlFor="question" className="form-label">Your Question:</label>
          <textarea
            id="question"
            className="form-control"
            rows="3"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="e.g., Why isn't 'international licensing' listed as a theme?"
          ></textarea>
        </div>
        <button type="submit" className="btn btn-danger" disabled={loading}>
          {loading ? (
            <>
              <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
              Getting Answer...
            </>
          ) : (
            'Ask Question'
          )}
        </button>
      </form>

      {error && (
        <div className="alert alert-danger mt-4" role="alert">
          {error}
        </div>
      )}

      {answer && (
        <div className="answer-container mt-4">
          <h3 className="mb-3">Answer</h3>
          <div className="mb-3">
            <strong>Question:</strong> {answer.question}
          </div>
          <div className="mb-4">
            <strong>Answer:</strong>
            <div style={{ whiteSpace: 'pre-line' }}>{answer.answer}</div>
          </div>
          {answer.sources && answer.sources.length > 0 && (
            <div className="source-citation">
              <strong>Sources:</strong>
              <ul className="list-unstyled">
                {answer.sources.map((source, index) => (
                  <li key={index}>{source}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      <div className="mt-5">
        <h4>Example Questions</h4>
        <p className="text-muted">Click on any example to use it:</p>
        <div className="list-group">
          {exampleQuestions.map((exampleQuestion, index) => (
            <button
              key={index}
              className="list-group-item list-group-item-action"
              onClick={() => handleExampleClick(exampleQuestion)}
            >
              {exampleQuestion}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default QuestionsPage;
