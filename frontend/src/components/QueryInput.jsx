import React, { useState, useRef, useEffect } from 'react';
import './QueryInput.css';

const QueryInput = ({ onSubmit, isLoading }) => {
  const [query, setQuery] = useState('');
  const textareaRef = useRef(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim() && !isLoading) {
      onSubmit(query.trim());
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  // Auto-resize textarea
  useEffect(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = `${Math.min(textarea.scrollHeight, 200)}px`;
    }
  }, [query]);

  return (
    <div className="query-input-container">
      <form onSubmit={handleSubmit} className="query-form">
        <div className="query-input-wrapper">
          <textarea
            ref={textareaRef}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="ENTER YOUR QUERY HERE..."
            className="query-input"
            rows={1}
            disabled={isLoading}
          />
        </div>
        <button
          type="submit"
          className="submit-button"
          disabled={!query.trim() || isLoading}
        >
          {isLoading ? '...' : 'SEND'}
        </button>
      </form>
    </div>
  );
};

export default QueryInput;
