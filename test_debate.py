#!/usr/bin/env python3
"""
Test script for Council of Frontiers debate system.
Run this to verify your setup before the demo.
"""
import asyncio
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.debate_orchestrator import DebateOrchestrator
from app.core.config import get_settings


async def test_debate(query: str):
    """Run a test debate and print results."""
    print("=" * 60)
    print(f"Testing: {query[:50]}...")
    print("=" * 60)
    
    settings = get_settings()
    
    # Check API keys
    if not settings.groq_api_key:
        print("❌ GROQ_API_KEY not set")
        return
    if not settings.cerebras_api_key:
        print("⚠️  CEREBRAS_API_KEY not set (will use Groq fallback)")
    
    print(f"✓ Groq configured: {settings.groq_model_primary}")
    print(f"✓ Cerebras configured: {settings.cerebras_model_primary}")
    print()
    
    orchestrator = DebateOrchestrator()
    
    try:
        async for message in orchestrator.run_debate(query):
            if message["type"] == "progress":
                print(f"[{message['stage']}] {message['message']}")
                
            elif message["type"] == "complete":
                result = message["result"]
                print()
                print("=" * 60)
                print("FINAL RESULT")
                print("=" * 60)
                print(f"Problem Type: {result['problem_type']}")
                print(f"Confidence: {result['confidence_score']:.2%}")
                print(f"Similarity: {result['similarity_score']:.2%}")
                print(f"Latency: {result['total_latency']:.1f}s")
                print(f"Early Stopped: {result['early_stopped']}")
                print()
                print("FINAL ANSWER:")
                print("-" * 60)
                print(result['final_answer'][:500] + "..." if len(result['final_answer']) > 500 else result['final_answer'])
                print()
                
            elif message["type"] == "error":
                print(f"❌ Error: {message['message']}")
                
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await orchestrator.close()


async def main():
    """Run test debates."""
    test_queries = [
        "Calculate the 10th Fibonacci number",
        "Write a Python function to check if a number is prime",
        "If A says B is lying, and B says C is lying, who is telling the truth?",
    ]
    
    print("\n🧪 Council of Frontiers - Test Suite\n")
    
    for i, query in enumerate(test_queries, 1):
        await test_debate(query)
        if i < len(test_queries):
            print("\n" + "=" * 60)
            print(f"Next test in 5 seconds...")
            print("=" * 60 + "\n")
            await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())
