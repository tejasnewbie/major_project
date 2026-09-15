#!/usr/bin/env python3
"""Test GPT-OSS on Groq."""
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv("backend/.env")

api_key = os.getenv("GROQ_API_KEY", "").strip()
client = Groq(api_key=api_key)

print("Testing openai/gpt-oss-120b on Groq...")

try:
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": "What is 2+2?"}],
        model="openai/gpt-oss-120b",
        max_tokens=50
    )
    content = chat_completion.choices[0].message.content
    print(f"✅ Success! Response: {content[:50]}")
except Exception as e:
    print(f"❌ Error: {e}")
