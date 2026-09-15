import React from 'react';
import './ProgressBar.css';

const steps = [
  { id: 'classification', label: 'Analyzing problem type' },
  { id: 'round1_start', label: 'Generation: Creating solutions' },
  { id: 'round1_progress', label: 'Generating solutions' },
  { id: 'evaluation', label: 'Evaluating solutions' },
  { id: 'execution', label: 'Testing code' },
  { id: 'winner_selected', label: 'Selecting best solution' },
  { id: 'refinement_start', label: 'Refinement: Improving winner' },
  { id: 'refinement_progress', label: 'Improving solution' },
  { id: 'synthesis_start', label: 'Synthesis: Finalizing answer' },
  { id: 'early_stop', label: 'Optimizing output' },
  { id: 'complete', label: 'Complete' },
];

const ProgressBar = ({ currentStage, messages }) => {
  const getStepStatus = (stepId) => {
    const relevant = messages.filter(m => m.stage === stepId);
    if (relevant.length === 0) return 'pending';
    
    const isCurrent = currentStage === stepId;
    const isComplete = messages.some(m => 
      m.stage === 'complete' || 
      (stepId !== 'complete' && m.stage === stepId && !isCurrent)
    );
    
    if (isComplete) return 'complete';
    if (isCurrent) return 'active';
    return 'pending';
  };

  return (
    <div className="progress-bar">
      {steps.map((step) => {
        const status = getStepStatus(step.id);
        if (status === 'pending') return null;
        
        const isActive = status === 'active';
        const isComplete = status === 'complete';
        
        return (
          <div 
            key={step.id}
            className={`progress-step progress-step--${status}`}
          >
            <div className="progress-icon">
              {isComplete ? '✓' : isActive ? <div className="spinner" /> : '○'}
            </div>
            <span className="progress-text">{step.label}</span>
          </div>
        );
      })}
    </div>
  );
};

export default ProgressBar;
