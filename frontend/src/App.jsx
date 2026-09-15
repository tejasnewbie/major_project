import React, { useState, useEffect, useCallback, useMemo } from 'react';
import QueryInput from './components/QueryInput';
import CollapsibleRound from './components/CollapsibleRound';
import FinalAnswer from './components/FinalAnswer';
import ThinkingBar from './components/ThinkingBar';
import { useWebSocket } from './hooks/useWebSocket';
import './App.css';

function App() {
  const { isConnected, messages, isLoading, connect, disconnect, sendQuery } = useWebSocket();
  const [result, setResult] = useState(null);
  const [round1Responses, setRound1Responses] = useState([]);
  const [refinementResponses, setRefinementResponses] = useState([]);
  const [scores, setScores] = useState([]);
  const [currentStage, setCurrentStage] = useState(null);
  const [category, setCategory] = useState(null);
  const [progressMessage, setProgressMessage] = useState('');
  const [startTime, setStartTime] = useState(null);

  useEffect(() => {
    connect();
    return () => disconnect();
  }, [connect, disconnect]);

  useEffect(() => {
    messages.forEach(msg => {
      if (msg.stage) {
        setCurrentStage(msg.stage);
      }
      if (msg.message) {
        setProgressMessage(msg.message);
      }

      if (msg.type === 'complete' && msg.result) {
        const data = msg.result;
        setResult(data);
        setRound1Responses(data.round1 || []);
        setRefinementResponses(data.refinements || []);
        setScores(data.scores || []);
        setCategory(data.category);
      }
    });
  }, [messages]);

  const handleSubmit = useCallback((query) => {
    setResult(null);
    setRound1Responses([]);
    setRefinementResponses([]);
    setScores([]);
    setCategory(null);
    setCurrentStage('classification');
    setStartTime(Date.now());
    sendQuery(query);
  }, [sendQuery]);

  // Calculate elapsed time
  const elapsedTime = useMemo(() => {
    if (!startTime || !isLoading) return 0;
    return Math.floor((Date.now() - startTime) / 1000);
  }, [startTime, isLoading]);

  // Determine round status
  const isRound1Complete = round1Responses.length === 3;
  const isRound1Active = isLoading && round1Responses.length > 0 && round1Responses.length < 3;

  const isRefinementComplete = refinementResponses.length >= 2;
  const isRefinementActive = isLoading && round1Responses.length === 3 && !isRefinementComplete;

  // Prepare agents for thinking bar
  const thinkingAgents = useMemo(() => {
    if (currentStage?.includes('round1')) {
      return [
        { name: 'NVIDIA', done: round1Responses.length >= 1, active: round1Responses.length === 0 },
        { name: 'Groq', done: round1Responses.length >= 2, active: round1Responses.length === 1 },
        { name: 'OpenRouter', done: round1Responses.length >= 3, active: round1Responses.length === 2 }
      ];
    }
    if (currentStage?.includes('refinement')) {
      return [
        { name: 'Refiner 1', done: refinementResponses.length >= 1, active: refinementResponses.length === 0 },
        { name: 'Refiner 2', done: refinementResponses.length >= 2, active: refinementResponses.length === 1 }
      ];
    }
    return [];
  }, [currentStage, round1Responses.length, refinementResponses.length]);

  const hasStarted = isLoading || result || round1Responses.length > 0;

  return (
    <div className="app">
      <div className={`connection-status connection-status--${isConnected ? 'connected' : 'disconnected'}`}>
        {isConnected ? 'Connected' : 'Disconnected'}
      </div>

      <header className={`header ${hasStarted ? 'header--compact' : ''}`}>
        <h1 className="title">
          Council<span className="title__accent">.</span>
        </h1>
        {!hasStarted && (
          <p className="subtitle">
            Multi-agent verification through collaborative debate.
          </p>
        )}
        {category && (
          <div className="category-badge">
            <span>◈</span>
            {category}
          </div>
        )}
      </header>

      <main className="main-content">
        <QueryInput onSubmit={handleSubmit} isLoading={isLoading} />

        {isLoading && (
          <ThinkingBar
            stage={currentStage}
            message={progressMessage}
            agents={thinkingAgents}
            progress={elapsedTime}
          />
        )}

        {/* Round 1: Generation */}
        {(round1Responses.length > 0 || isLoading) && (
          <div className="rounds-container">
            <CollapsibleRound
              number={1}
              title="Generation"
              agents={round1Responses.length > 0 ? round1Responses : [
                { provider: 'nvidia' }, { provider: 'groq' }, { provider: 'open_router' }
              ]}
              isComplete={isRound1Complete}
              isActive={isRound1Active}
              scores={scores}
            />

            {/* Round 2: Refinement */}
            {(refinementResponses.length > 0 || (isLoading && isRound1Complete)) && (
              <CollapsibleRound
                number={2}
                title="Refinement"
                agents={refinementResponses.length > 0 ? refinementResponses : [
                  { provider: 'nvidia' }, { provider: 'groq' }
                ]}
                isComplete={isRefinementComplete}
                isActive={isRefinementActive}
              />
            )}
          </div>
        )}

        {/* Final Answer */}
        {result && (
          <FinalAnswer
            answer={result?.final_answer}
            confidence={result?.confidence}
            latency={result?.latency}
            earlyStopped={result?.early_stopped}
          />
        )}

        {!hasStarted && (
          <div className="empty-state">
            <div className="empty-state__icon">◈</div>
            <div className="empty-state__title">What would you like to solve?</div>
            <p className="empty-state__text">
              The Council brings together multiple AI models to debate and refine solutions.
            </p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
