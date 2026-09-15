import React, { useState } from 'react';
import CodeBlock from './CodeBlock';
import './FinalAnswer.css';

const FinalAnswer = ({ answer, confidence, latency, earlyStopped }) => {
  const [showThinking, setShowThinking] = useState(false);
  const [copied, setCopied] = useState(false);
  
  const safeAnswer = answer || 'No answer generated';
  const safeConfidence = confidence || 0;
  const safeLatency = latency || 0;
  
  // Extract thinking and final answer
  const extractSections = (text) => {
    if (!text) return { final: text, thinking: null };
    
    // Check for Kimi K2.5 thinking format
    const thinkingMatch = text.match(/<!--\s*Thinking\s*-->([\s\S]*?)<!--\s*Final Answer\s*-->/i);
    const finalMatch = text.match(/<!--\s*Final Answer\s*-->([\s\S]*)$/i);
    
    if (thinkingMatch && finalMatch) {
      return {
        final: finalMatch[1].trim(),
        thinking: thinkingMatch[1].trim()
      };
    }
    
    // Check for SOLUTION/REASONING format
    const solMatch = text.match(/SOLUTION[:\s]*\n?([\s\S]+?)(?=REASONING|CONFIDENCE|$)/i);
    const reasonMatch = text.match(/REASONING[:\s]*\n?([\s\S]+)$/i);
    
    if (solMatch) {
      return {
        final: solMatch[1].trim(),
        thinking: reasonMatch ? reasonMatch[1].trim() : null
      };
    }
    
    return { final: text, thinking: null };
  };
  
  const sections = extractSections(safeAnswer);
  
  // Parse content with code blocks
  const renderContent = (text) => {
    if (!text) return <span className="text-muted">No content</span>;
    
    const parts = text.split(/(```[\w]*\n?[\s\S]*?```)/g);
    
    return parts.map((part, index) => {
      if (part.startsWith('```')) {
        // Extract language and optional filename
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
        // Fallback for simple code blocks
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
      
      // Regular text - process inline code and formatting
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

  const getQualityLabel = (score) => {
    if (score >= 0.85) return 'Excellent';
    if (score >= 0.70) return 'Good';
    if (score >= 0.55) return 'Fair';
    return 'Needs Work';
  };

  const getQualityClass = (score) => {
    if (score >= 0.85) return 'quality--excellent';
    if (score >= 0.70) return 'quality--good';
    if (score >= 0.55) return 'quality--fair';
    return 'quality--low';
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(sections.final);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="final-answer animate-fade-up">
      {/* Header */}
      <div className="final-header">
        <div className="final-brand">
          <div className="final-logo">
            <span className="final-logo__icon">◈</span>
          </div>
          <div className="final-title-group">
            <h2 className="final-title">Final Answer</h2>
            <span className="final-subtitle">Synthesized from multiple perspectives</span>
          </div>
        </div>
        
        <div className="final-actions">
          <div className={`quality-badge ${getQualityClass(safeConfidence)}`}>
            <span className="quality-badge__label">{getQualityLabel(safeConfidence)}</span>
            <span className="quality-badge__score">{(safeConfidence * 100).toFixed(0)}%</span>
          </div>
          
          <button 
            className={`copy-btn ${copied ? 'copy-btn--copied' : ''}`}
            onClick={handleCopy}
          >
            {copied ? (
              <>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
                <span>Copied</span>
              </>
            ) : (
              <>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                  <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                </svg>
                <span>Copy</span>
              </>
            )}
          </button>
        </div>
      </div>
      
      {/* Content */}
      <div className="final-content">
        {renderContent(sections.final)}
      </div>
      
      {/* Thinking Process (Collapsible) */}
      {sections.thinking && (
        <div className="thinking-panel">
          <button 
            className="thinking-panel__toggle"
            onClick={() => setShowThinking(!showThinking)}
          >
            <div className="thinking-panel__left">
              <div className="thinking-panel__icon">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M12 2a10 10 0 1 0 10 10 4 4 0 0 1-5-5 4 4 0 0 1-5-5" />
                  <path d="M8.5 8.5v.01" />
                  <path d="M16 15.5v.01" />
                </svg>
              </div>
              <span className="thinking-panel__label">Thinking Process</span>
            </div>
            <svg 
              className={`thinking-panel__chevron ${showThinking ? 'thinking-panel__chevron--open' : ''}`}
              width="16" 
              height="16" 
              viewBox="0 0 24 24" 
              fill="none" 
              stroke="currentColor" 
              strokeWidth="2"
            >
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </button>
          
          {showThinking && (
            <div className="thinking-panel__content animate-fade-up">
              <pre className="thinking-text">{sections.thinking}</pre>
            </div>
          )}
        </div>
      )}
      
      {/* Footer */}
      <div className="final-footer">
        <div className="final-meta">
          <span className="final-meta__item">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="10"></circle>
              <polyline points="12 6 12 12 16 14"></polyline>
            </svg>
            {safeLatency.toFixed(1)}s
          </span>
          {earlyStopped && (
            <span className="final-meta__badge">
              Early Stop
            </span>
          )}
        </div>
        <div className="final-branding">
          <span>Generated by Council</span>
        </div>
      </div>
    </div>
  );
};

export default FinalAnswer;
