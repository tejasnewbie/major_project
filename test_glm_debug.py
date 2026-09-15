#!/usr/bin/env python3
"""Debug GLM specifically."""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv("backend/.env")

api_key = os.getenv("NVIDIA_API_KEY", "").strip().replace('"', '')

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key
)

print("="*60)
print("Testing GLM with different parameters")
print("="*60)

# Test 1: With enable_thinking
print("\n--- Test 1: With enable_thinking=True, clear_thinking=False ---")
try:
    completion = client.chat.completions.create(
        model="z-ai/glm4.7",
        messages=[{"role": "user", "content": "What is 2+2?"}],
        temperature=1.0,
        top_p=1.0,
        max_tokens=50,
        extra_body={"chat_template_kwargs": {"enable_thinking": True, "clear_thinking": False}}
    )
    print(f"✅ Success!")
    print(f"Response: {completion}")
    if completion.choices:
        msg = completion.choices[0].message
        print(f"Content: {getattr(msg, 'content', None)}")
        print(f"Reasoning: {getattr(msg, 'reasoning_content', None)}")
except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Without extra_body
print("\n--- Test 2: Without extra_body ---")
try:
    completion = client.chat.completions.create(
        model="z-ai/glm4.7",
        messages=[{"role": "user", "content": "What is 2+2?"}],
        temperature=0.7,
        max_tokens=50
    )
    print(f"✅ Success!")
    print(f"Response: {completion}")
    if completion.choices:
        msg = completion.choices[0].message
        print(f"Content: {getattr(msg, 'content', None)}")
        print(f"Reasoning: {getattr(msg, 'reasoning_content', None)}")
except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

# Test 3: With thinking=True (like deepseek)
print("\n--- Test 3: With thinking=True ---")
try:
    completion = client.chat.completions.create(
        model="z-ai/glm4.7",
        messages=[{"role": "user", "content": "What is 2+2?"}],
        temperature=0.7,
        max_tokens=50,
        extra_body={"chat_template_kwargs": {"thinking": True}}
    )
    print(f"✅ Success!")
    print(f"Response: {completion}")
    if completion.choices:
        msg = completion.choices[0].message
        print(f"Content: {getattr(msg, 'content', None)}")
        print(f"Reasoning: {getattr(msg, 'reasoning_content', None)}")
except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
