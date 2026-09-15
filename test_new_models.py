#!/usr/bin/env python3
"""Test NEW model configurations before implementing."""
import asyncio
import os
import time
from dotenv import load_dotenv

load_dotenv("backend/.env")

TEST_PROMPT = "What is 2+2? Answer in one word."

# NEW MODELS TO TEST
CEREBRAS_MODELS = [
    ("qwen-3-235b-a22b-instruct-2507", "qwen-235b"),
    ("gpt-oss-120b", "gpt-oss"),
    ("llama-3.3-70b", "llama-70b"),
]

GROQ_MODELS = [
    ("moonshotai/kimi-k2-instruct", "kimi-k2"),
    ("meta-llama/llama-4-maverick-17b-128e-instruct", "llama-4-maverick"),
    ("llama-3.3-70b-versatile", "llama-3.3"),
]


async def test_cerebras():
    """Test Cerebras models."""
    print("\n" + "="*70)
    print("TESTING CEREBRAS MODELS")
    print("="*70)
    
    from cerebras.cloud.sdk import Cerebras
    
    api_key = os.getenv("CEREBRAS_API_KEY", "").strip()
    if not api_key or api_key == "your_cerebras_api_key_here":
        print("❌ CEREBRAS_API_KEY not set")
        return False
    
    client = Cerebras(api_key=api_key)
    all_passed = True
    
    for model, short_name in CEREBRAS_MODELS:
        print(f"\n🧪 Testing: {short_name}")
        print(f"   Model ID: {model}")
        start = time.time()
        try:
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": TEST_PROMPT}],
                model=model
            )
            elapsed = time.time() - start
            content = chat_completion.choices[0].message.content
            print(f"   ✅ {elapsed:.1f}s - Response: {content[:50]}")
        except Exception as e:
            elapsed = time.time() - start
            print(f"   ❌ {elapsed:.1f}s - Error: {e}")
            all_passed = False
    
    return all_passed


async def test_groq():
    """Test Groq models."""
    print("\n" + "="*70)
    print("TESTING GROQ MODELS")
    print("="*70)
    
    from groq import Groq
    
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key or api_key == "your_groq_api_key_here":
        print("❌ GROQ_API_KEY not set")
        return False
    
    client = Groq(api_key=api_key)
    all_passed = True
    
    for model, short_name in GROQ_MODELS:
        print(f"\n🧪 Testing: {short_name}")
        print(f"   Model ID: {model}")
        start = time.time()
        try:
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": TEST_PROMPT}],
                model=model,
                max_tokens=50
            )
            elapsed = time.time() - start
            content = chat_completion.choices[0].message.content
            print(f"   ✅ {elapsed:.1f}s - Response: {content[:50]}")
        except Exception as e:
            elapsed = time.time() - start
            print(f"   ❌ {elapsed:.1f}s - Error: {e}")
            all_passed = False
    
    return all_passed


async def main():
    """Run all tests."""
    print("\n🔬 TESTING NEW MODEL CONFIGURATIONS")
    print("="*70)
    print("\nThis will verify all new models work before updating main code.")
    print("="*70)
    
    cerebras_ok = await test_cerebras()
    groq_ok = await test_groq()
    
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Cerebras: {'✅ All passed' if cerebras_ok else '❌ Some failed'}")
    print(f"Groq:     {'✅ All passed' if groq_ok else '❌ Some failed'}")
    
    if cerebras_ok and groq_ok:
        print("\n🎉 All models working! Safe to update config.py")
    else:
        print("\n⚠️  Some models failed. Check errors above.")
        print("   Do NOT update config.py until all models pass.")
    
    print("="*70)


if __name__ == "__main__":
    asyncio.run(main())
