"""API routes for the Council of Frontiers."""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import json
import logging

from app.services.debate_orchestrator import DebateOrchestrator
from app.core.config import get_settings

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    settings = get_settings()
    groq_keys = settings.get_groq_api_keys()
    open_router_keys = settings.get_open_router_api_keys()
    nvidia_keys = settings.get_nvidia_api_keys()
    return {
        "status": "healthy",
        "providers_configured": {
            "groq": len(groq_keys) > 0,
            "open_router": len(open_router_keys) > 0,
            "nvidia": len(nvidia_keys) > 0
        },
        "key_counts": {
            "groq": len(groq_keys),
            "open_router": len(open_router_keys),
            "nvidia": len(nvidia_keys)
        }
    }


@router.get("/config")
async def get_config():
    """Get current configuration (without sensitive data)."""
    settings = get_settings()
    return {
        "groq_models": {
            "primary": settings.groq_model_primary,
            "secondary": settings.groq_model_secondary,
            "fallback": settings.groq_model_fallback
        },
        "open_router_models": {
            "primary": settings.open_router_model_primary,
            "secondary": settings.open_router_model_secondary,
            "fallback": settings.open_router_model_fallback
        },
        "nvidia_models": {
            "primary": settings.nvidia_model_primary,
            "secondary": settings.nvidia_model_secondary,
            "tertiary": settings.nvidia_model_tertiary
        },
        "rate_limits": {
            "groq": settings.groq_rate_limit,
            "open_router": settings.open_router_rate_limit,
            "nvidia": settings.nvidia_rate_limit
        },
        "features": {
            "early_stopping": settings.enable_early_stopping,
            "similarity_threshold": settings.similarity_threshold
        }
    }


@router.post("/debate")
async def run_debate(query: str, problem_type: Optional[str] = None):
    """
    Run a debate synchronously (non-streaming).
    
    Args:
        query: The problem/query to solve
        problem_type: Optional override ('math', 'code', 'logic', 'general')
    
    Returns:
        Complete debate result
    """
    orchestrator = DebateOrchestrator()
    
    try:
        results = []
        async for message in orchestrator.run_debate(query, stream=True):
            if message["type"] == "complete":
                return message["result"]
            results.append(message)
        
        # Should not reach here
        return {"error": "Debate completed without final result"}
        
    except Exception as e:
        logger.error(f"Debate error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await orchestrator.close()


@router.websocket("/ws/debate")
async def debate_websocket(websocket: WebSocket):
    """
    WebSocket endpoint for real-time debate streaming.
    
    Expected message format:
    {
        "query": "problem to solve",
        "problem_type": "optional override"
    }
    """
    await websocket.accept()
    orchestrator = None
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            query = message.get("query")
            if not query:
                await websocket.send_json({
                    "type": "error",
                    "message": "Query is required"
                })
                continue
            
            # Run debate with streaming
            orchestrator = DebateOrchestrator()
            
            async for update in orchestrator.run_debate(query, stream=True):
                await websocket.send_json(update)
            
            await orchestrator.close()
            orchestrator = None
            
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        try:
            await websocket.send_json({
                "type": "error",
                "message": str(e)
            })
        except:
            pass
    finally:
        if orchestrator:
            await orchestrator.close()


@router.post("/execute")
async def execute_code(code: str, test_cases: Optional[list] = None):
    """
    Execute code in the sandbox (for testing).
    
    Args:
        code: Python code to execute
        test_cases: Optional test inputs
    
    Returns:
        Execution results
    """
    from app.services.code_executor import get_executor
    
    executor = get_executor()
    result = await executor.execute(code, test_cases=test_cases)
    
    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "exit_code": result.exit_code,
        "execution_time": result.execution_time,
        "error": result.error
    }


@router.get("/examples")
async def get_examples():
    """Get example queries for testing."""
    return {
        "math": [
            "Calculate the 20th Fibonacci number",
            "Solve: x^2 + 5x + 6 = 0",
            "What is the probability of rolling a sum of 7 with two dice?"
        ],
        "code": [
            "Write a Python function to reverse a linked list",
            "Implement quicksort algorithm",
            "Create a function to check if a string is a valid palindrome"
        ],
        "logic": [
            "Three people are lying. A says B is lying. B says C is lying. C says both A and B are lying. Who is telling the truth?",
            "If all roses are flowers and some flowers fade quickly, can we conclude that some roses fade quickly?"
        ],
        "general": [
            "Explain how blockchain works",
            "What are the tradeoffs between SQL and NoSQL databases?"
        ]
    }
