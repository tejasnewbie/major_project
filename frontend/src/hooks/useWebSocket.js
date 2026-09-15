import { useState, useCallback, useRef, useEffect } from 'react';

export const useWebSocket = () => {
  const [isConnected, setIsConnected] = useState(false);
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const ws = useRef(null);

  const connect = useCallback(() => {
    const wsUrl = process.env.REACT_APP_WS_URL || 'ws://localhost:8000/api/ws/debate';
    
    ws.current = new WebSocket(wsUrl);
    
    ws.current.onopen = () => {
      setIsConnected(true);
      console.log('WebSocket connected');
    };
    
    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setMessages((prev) => [...prev, data]);
      
      if (data.type === 'complete' || data.type === 'error') {
        setIsLoading(false);
      }
    };
    
    ws.current.onclose = () => {
      setIsConnected(false);
      console.log('WebSocket disconnected');
    };
    
    ws.current.onerror = (error) => {
      console.error('WebSocket error:', error);
      setIsLoading(false);
    };
  }, []);

  const disconnect = useCallback(() => {
    if (ws.current) {
      ws.current.close();
    }
  }, []);

  const sendQuery = useCallback((query, problemType = null) => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      setIsLoading(true);
      setMessages([]);
      ws.current.send(JSON.stringify({
        query,
        problem_type: problemType
      }));
    } else {
      console.error('WebSocket not connected');
    }
  }, []);

  useEffect(() => {
    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, []);

  return {
    isConnected,
    messages,
    isLoading,
    connect,
    disconnect,
    sendQuery
  };
};
