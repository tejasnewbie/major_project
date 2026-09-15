#!/usr/bin/env python3
"""Simple NVIDIA test with full error details."""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv("backend/.env")

api_key = os.getenv("NVIDIA_API_KEY", "").strip().replace('"', '')
print(f"API Key (first 20 chars): {api_key[:20]}...")

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key
)

# Test deepseek
print("\n" + "="*60)
print("Testing deepseek-ai/deepseek-v3.1")
print("="*60)

try:
    completion = client.chat.completions.create(
        model="deepseek-ai/deepseek-v3.1",
        messages=[{"role": "user", "content": "What is 2+2?"}],
        temperature=0.2,
        top_p=0.7,
        max_tokens=50,
        extra_body={"chat_template_kwargs": {"thinking": True}}
    )
    
    print(f"✅ Success!")
    print(f"Type: {type(completion)}")
    print(f"Has choices attr: {hasattr(completion, 'choices')}")
    
    if hasattr(completion, 'choices'):
        print(f"Choices type: {type(completion.choices)}")
        print(f"Choices value: {completion.choices}")
        
        if completion.choices:
            choice = completion.choices[0]
            print(f"\nChoice: {choice}")
            print(f"Choice type: {type(choice)}")
            
            if hasattr(choice, 'message'):
                print(f"Message: {choice.message}")
                if choice.message:
                    print(f"Content: {choice.message.content}")
                else:
                    print("❌ message is None")
            else:
                print(f"❌ No message attr. Attrs: {dir(choice)}")
        else:
            print("❌ choices is empty")
    else:
        print(f"❌ No choices. Attrs: {dir(completion)}")
        
except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
