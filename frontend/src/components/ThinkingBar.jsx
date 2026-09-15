import React from 'react';
import './ThinkingBar.css';

const ThinkingBar = ({ stage, message, agents, progress }) => {
  // Get stage label
  const getStageLabel = () => {
    const labels = {
      classification: 'ANALYZING INPUT',
      round1_start: 'GENERATING RESPONSES',
      round1_progress: 'GENERATING RESPONSES',
      evaluation: 'SCORING OUTPUTS',
      execution: 'EXECUTING CODE',
      winner_selected: 'REFINING ANSWER',
      refinement_start: 'REFINING ANSWER',
      refinement_progress: 'REFINING ANSWER',
      synthesis_start: 'SYNTHESIZING FINAL ANSWER',
      complete: 'PROCESS COMPLETE'
    };
    return labels[stage] || 'PROCESSING';
  };

  // Get thinking time display
  const getThinkingTime = () => {
    if (!progress) return '0s';
    return `${progress}s`;
  };

  return (
    <div className="thinking-bar">
      <div className="thinking-header">
        <span className="thinking-stage">[{getStageLabel()}]</span>
        <span className="thinking-timer">{getThinkingTime()}</span>
      </div>

      <div className="progress-container">
        <div
          className="progress-fill"
          style={{ width: '100%' }} // Always full width with animation for now, or use progress logic if granular
        />
      </div>

      {message && (
        <div className="thinking-message">
          &gt; {message}
        </div>
      )}

      {agents && agents.length > 0 && (
        <div className="agents-grid">
          {agents.map((agent, i) => (
            <div
              key={i}
              className={`thinking-agent ${agent.done ? 'done' : agent.active ? 'active' : ''}`}
            >
              {agent.name.toUpperCase()}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ThinkingBar;
