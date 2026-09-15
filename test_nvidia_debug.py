#!/usr/bin/env python3
"""Debug NVIDIA NIM response structure."""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv("backend/.env")

api_key = os.getenv("NVIDIA_API_KEY", "").strip()
if not api_key:
    print("❌ NVIDIA_API_KEY not set")
    exit(1)

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key
)

models = [
    "deepseek-ai/deepseek-v3.1",
    "z-ai/glm4.7"
]

for model in models:
    print(f"\n{'='*60}")
    print(f"Testing: {model}")
    print('='*60)
    
    # Model-specific params
    if "glm" in model.lower():
        extra_body = {"chat_template_kwargs": {"enable_thinking": True, "clear_thinking": False}}
        temp = 1.0
        top_p = 1.0
    elif "deepseek" in model.lower():
        extra_body = {"chat_template_kwargs": {"thinking": True}}
        temp = 0.2
        top_p = 0.7
    else:
        extra_body = {}
        temp = 0.7
        top_p = 1.0
    
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "What is 2+2? Answer in one word."}],
            temperature=temp,
            top_p=top_p,
            max_tokens=50,
            extra_body=extra_body
        )
        
        print(f"✅ Response received!")
        print(f"\nResponse object: {completion}")
        print(f"Response type: {type(completion)}")
        print(f"\nResponse dict: {completion.__dict__ if hasattr(completion, '__dict__') else 'N/A'}")
        
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
