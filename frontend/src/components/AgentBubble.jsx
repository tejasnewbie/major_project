import React from 'react';
import './AgentBubble.css';

const getAgentLabel = (agentId) => {
  if (!agentId) return 'Agent';
  const type = agentId.includes('agent') ? 'Solver' : 
               agentId.includes('critic') ? 'Critic' : 
               agentId.includes('refiner') ? 'Refiner' : 'Agent';
  const parts = agentId.split('_');
  const num = parts[1] || '?';
  return `${type} ${num}`;
};

const AgentBubble = ({ agentId, provider, model, reasoningStyle, content, latency, isThinking }) => {
  // Handle undefined content
  const safeContent = content || '';
  const safeAgentId = agentId || 'unknown_0';
  const safeProvider = provider || 'unknown';
  
  const renderContent = (text) => {
    if (!text) return <span>No content</span>;
    
    const parts = text.split(/(```[\s\S]*?```)/);
    
    return parts.map((part, index) => {
      if (part.startsWith('```')) {
        const code = part.replace(/```[\w]*\n?/, '').replace(/```$/, '');
        return <pre key={index}><code>{code}</code></pre>;
      }
      return <span key={index}>{part}</span>;
    });
  };

  // Get avatar number safely
  const avatarNum = safeAgentId.split('_')[1] || '?';

  return (
    <div className="agent-bubble">
      <div className="agent-header">
        <div className={`agent-avatar agent-avatar--${safeAgentId}`}>
          {avatarNum}
        </div>
        <div className="agent-info">
          <span className="agent-name">{getAgentLabel(safeAgentId)}</span>
          <div className="agent-badges">
            <span className="badge badge--provider" data-provider={safeProvider}>
              {safeProvider}
            </span>
            {reasoningStyle && (
              <span className="badge badge--style">{reasoningStyle}</span>
            )}
            {latency > 0 && (
              <span className="badge badge--latency">{latency.toFixed(1)}s</span>
            )}
          </div>
        </div>
      </div>
      
      {isThinking ? (
        <div className="agent-thinking">
          <span>Thinking</span>
          <span className="thinking-dots">
            <span></span>
            <span></span>
            <span></span>
          </span>
        </div>
      ) : (
        <div className="agent-content">
          {renderContent(safeContent)}
        </div>
      )}
    </div>
  );
};

export default AgentBubble;
