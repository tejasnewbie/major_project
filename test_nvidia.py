#!/usr/bin/env python3
"""Test NVIDIA NIM API directly."""
import asyncio
import httpx
import os
from dotenv import load_dotenv

load_dotenv("backend/.env")

async def test_nvidia():
    api_key = os.getenv("NVIDIA_API_KEY", "").strip()
    
    print("=" * 60)
    print("Testing NVIDIA NIM API")
    print("=" * 60)
    print(f"API Key present: {'Yes' if api_key else 'No'}")
    print(f"API Key length: {len(api_key)}")
    print()
    
    if not api_key:
        print("❌ NVIDIA_API_KEY not found in .env")
        return
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    models_to_test = [
        ("deepseek-ai/deepseek-v3.2", {"thinking": True}),
        ("moonshotai/kimi-k2.5", {"thinking": True}),
        ("z-ai/glm4.7", {"enable_thinking": True, "clear_thinking": False})
    ]
    
    # Use 120s timeout for large models
    async with httpx.AsyncClient(timeout=120.0) as client:
        for model, template_kwargs in models_to_test:
            print(f"Testing: {model}")
            print(f"  chat_template_kwargs: {template_kwargs}")
            
            payload = {
                "model": model,
                "messages": [
                    {"role": "user", "content": "Say 'Hello' and nothing else."}
                ],
                "temperature": 0.7,
                "max_tokens": 50,
                "stream": False,
                "top_p": 1.0,
                "chat_template_kwargs": template_kwargs
            }
            
            try:
                start = asyncio.get_event_loop().time()
                response = await client.post(
                    "https://integrate.api.nvidia.com/v1/chat/completions",
                    headers=headers,
                    json=payload
                )
                elapsed = asyncio.get_event_loop().time() - start
                
                print(f"  Status: {response.status_code}")
                print(f"  Time: {elapsed:.1f}s")
                
                if response.status_code == 200:
                    data = response.json()
                    if "choices" in data and len(data["choices"]) > 0:
                        choice = data["choices"][0]
                        if "message" in choice and choice["message"]:
                            content = choice["message"].get("content", "")
                            print(f"  ✅ Response: {content[:100]}")
                        else:
                            print(f"  ⚠️  No message in choice: {choice}")
                    else:
                        print(f"  ⚠️  No choices in response: {data.keys()}")
                else:
                    print(f"  ❌ Error: {response.text[:500]}")
                    
            except httpx.TimeoutException:
                print(f"  ❌ Timeout after 120s")
            except Exception as e:
                print(f"  ❌ Exception: {type(e).__name__}: {e}")
            
            print()
            await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(test_nvidia())
