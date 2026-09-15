import React, { useState } from 'react';
import CodeBlock from './CodeBlock';
import './CollapsibleRound.css';

const CollapsibleRound = ({ 
  number, 
  title, 
  agents, 
  isComplete, 
  isActive,
  scores 
}) => {
  const [isOpen, setIsOpen] = useState(false);

  // Get status icon
  const getStatusIcon = () => {
    if (isComplete) return '✓';
    if (isActive) return '◐';
    return '○';
  };

  // Render thinking animation
  const renderThinking = () => (
    <div className="round-thinking">
      <div className="round-thinking__animation">
        <span className="round-thinking__dot"></span>
        <span className="round-thinking__dot"></span>
        <span className="round-thinking__dot"></span>
      </div>
      <span className="round-thinking__text">
        {isComplete ? 'Complete' : isActive ? 'Processing' : 'Waiting'}
      </span>
      {agents && agents.length > 0 && (
        <div className="round-agents-row">
          {agents.map((agent, i) => (
            <div 
              key={i} 
              className={`round-agent-pill ${agent.content ? 'round-agent-pill--done' : isActive ? 'round-agent-pill--active' : ''}`}
            >
              <span className="round-agent-pill__dot"></span>
              <span className="round-agent-pill__name">{agent.provider}</span>
              {scores && scores[i] && (
                <span className="round-agent-pill__score">{scores[i].score}/20</span>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );

  // Render content with code blocks
  const renderContent = (text) => {
    if (!text) return <span className="text-muted">No content</span>;
    
    const parts = text.split(/(```[\w]*\n?[\s\S]*?```)/g);
    
    return parts.map((part, index) => {
      if (part.startsWith('```')) {
        const match = part.match(/```(\w+)?(?::([^\n]*))?\n([\s\S]*?)```/);
        if (match) {
          const [, lang, filename, code] = match;
          return (
            <CodeBlock 
              key={index} 
              code={code.trim()} 
              language={lang || 'text'} 
              filename={filename || ''}
            />
          );
        }
        const simpleMatch = part.match(/```(\w*)\n?([\s\S]*?)```/);
        if (simpleMatch) {
          return (
            <CodeBlock 
              key={index} 
              code={simpleMatch[2].trim()} 
              language={simpleMatch[1] || 'text'} 
            />
          );
        }
      }
      
      const segments = part.split(/(\*\*[^*]+\*\*|`[^`]+`)/).map((segment, i) => {
        if (segment.startsWith('**') && segment.endsWith('**')) {
          return <strong key={i}>{segment.slice(2, -2)}</strong>;
        }
        if (segment.startsWith('`') && segment.endsWith('`')) {
          return <code key={i} className="inline-code">{segment.slice(1, -1)}</code>;
        }
        return <span key={i}>{segment}</span>;
      });
      
      return <span key={index}>{segments}</span>;
    });
  };

  // Render expanded content
  const renderExpanded = () => (
    <div className="round-expanded">
      <div className="round-agents-list">
        {agents.map((agent, i) => (
          <div key={i} className="round-agent-card">
            <div className="round-agent-header">
              <div className="round-agent-avatar">
                {(agent.agent || '').split('_')[1] || '?'}
              </div>
              <div className="round-agent-info">
                <span className="round-agent-name">
                  {agent.agent?.includes('agent') ? 'Solver' : 
                   agent.agent?.includes('refiner') ? 'Refiner' : 'Agent'}
                  {' '}{(agent.agent || '').split('_')[1] || '?'}
                </span>
                <span className="round-agent-model">{agent.model}</span>
              </div>
              <div className="round-agent-meta">
                <span className="round-agent-provider">{agent.provider}</span>
                {agent.latency > 0 && (
                  <span className="round-agent-latency">{agent.latency.toFixed(1)}s</span>
                )}
              </div>
            </div>
            <div className="round-agent-content">
              {renderContent(agent.content)}
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  return (
    <div 
      className={`round-card ${isOpen ? 'round-card--open' : ''}`}
      data-complete={isComplete}
      data-active={isActive}
    >
      <button 
        className="round-header"
        onClick={() => setIsOpen(!isOpen)}
      >
        <div className="round-header__left">
          <div className="round-number">
            {getStatusIcon()}
          </div>
          <div className="round-title-group">
            <span className="round-title">{title}</span>
            <span className="round-subtitle">
              {agents?.length || 0} agents
            </span>
          </div>
        </div>
        <div className="round-header__right">
          <span className="round-status-badge">
            {isComplete ? 'Done' : isActive ? 'Active' : 'Pending'}
          </span>
          <svg 
            className={`round-chevron ${isOpen ? 'round-chevron--open' : ''}`}
            width="16" 
            height="16" 
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            strokeWidth="2"
          >
            <polyline points="6 9 12 15 18 9"></polyline>
          </svg>
        </div>
      </button>
      
      {isOpen ? renderExpanded() : renderThinking()}
    </div>
  );
};

export default CollapsibleRound;
