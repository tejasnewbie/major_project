"""
Single unified test script to verify all LLM models and providers configured in .env.
Providers tested: Groq, OpenRouter, NVIDIA NIM.
"""
import os
import sys
import time
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# Locate and load .env file
ENV_PATH = Path(__file__).parent / "backend" / ".env"
if not ENV_PATH.exists():
    ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

TEST_PROMPT = "just say hi"
REQUEST_TIMEOUT = 30.0


async def test_groq_models():
    """Test all Groq models configured in .env."""
    print("\n" + "=" * 70)
    print(" 🚀 TESTING GROQ MODELS")
    print("=" * 70)
    
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        print("❌ GROQ_API_KEY not found in environment.")
        return []

    from groq import Groq
    client = Groq(api_key=api_key, timeout=REQUEST_TIMEOUT)

    models_to_test = [
        ("Primary", os.getenv("GROQ_MODEL_PRIMARY", "qwen/qwen3.8-27b")),
        ("Secondary", os.getenv("GROQ_MODEL_SECONDARY", "openai/gpt-oss-120b")),
        ("Fallback", os.getenv("GROQ_MODEL_FALLBACK", "openai/gpt-oss-20b")),
    ]

    results = []
    for role, model_name in models_to_test:
        print(f"\n[Groq] Testing {role}: {model_name}...")
        start_time = time.time()
        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda m=model_name: client.chat.completions.create(
                    model=m,
                    messages=[{"role": "user", "content": TEST_PROMPT}],
                    max_tokens=60,
                    temperature=0.3
                )
            )
            elapsed = time.time() - start_time
            content = response.choices[0].message.content.strip().replace("\n", " ")
            print(f"  ✅ SUCCESS ({elapsed:.2f}s): {content[:80]}")
            results.append({"provider": "Groq", "role": role, "model": model_name, "status": "PASS", "latency": f"{elapsed:.2f}s", "output": content[:60]})
        except Exception as err:
            elapsed = time.time() - start_time
            print(f"  ❌ FAILED ({elapsed:.2f}s): {type(err).__name__} - {err}")
            results.append({"provider": "Groq", "role": role, "model": model_name, "status": "FAIL", "latency": f"{elapsed:.2f}s", "output": str(err)[:60]})

    return results


async def test_openrouter_models():
    """Test all OpenRouter models configured in .env."""
    print("\n" + "=" * 70)
    print(" 🌐 TESTING OPENROUTER MODELS")
    print("=" * 70)
    
    api_key = os.getenv("OPEN_ROUTER_API_KEY", "").strip()
    if not api_key:
        print("❌ OPEN_ROUTER_API_KEY not found in environment.")
        return []

    from openai import OpenAI
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        timeout=REQUEST_TIMEOUT
    )

    models_to_test = [
        ("Primary", os.getenv("OPEN_ROUTER_MODEL_PRIMARY", "liquid/lfm-2.5-2.6b:free")),
        ("Secondary", os.getenv("OPEN_ROUTER_MODEL_SECONDARY", "nex-agi/nex-n2.5-mini:free")),
        ("Fallback", os.getenv("OPEN_ROUTER_MODEL_FALLBACK", "cohere/north-mini-code:free")),
    ]

    results = []
    for role, model_name in models_to_test:
        print(f"\n[OpenRouter] Testing {role}: {model_name}...")
        start_time = time.time()
        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda m=model_name: client.chat.completions.create(
                    model=m,
                    messages=[{"role": "user", "content": TEST_PROMPT}],
                    max_tokens=60,
                    temperature=0.3,
                    extra_headers={
                        "HTTP-Referer": "https://counciloffrontiers.local",
                        "X-Title": "Council of Frontiers Test"
                    }
                )
            )
            elapsed = time.time() - start_time
            content = (response.choices[0].message.content or "").strip().replace("\n", " ")
            print(f"  ✅ SUCCESS ({elapsed:.2f}s): {content[:80]}")
            results.append({"provider": "OpenRouter", "role": role, "model": model_name, "status": "PASS", "latency": f"{elapsed:.2f}s", "output": content[:60]})
        except Exception as err:
            elapsed = time.time() - start_time
            print(f"  ❌ FAILED ({elapsed:.2f}s): {type(err).__name__} - {err}")
            results.append({"provider": "OpenRouter", "role": role, "model": model_name, "status": "FAIL", "latency": f"{elapsed:.2f}s", "output": str(err)[:60]})

    return results


async def test_nvidia_models():
    """Test all NVIDIA NIM models configured in .env."""
    print("\n" + "=" * 70)
    print(" ⚡ TESTING NVIDIA NIM MODELS")
    print("=" * 70)
    
    api_key = os.getenv("NVIDIA_API_KEY", "").strip()
    if not api_key:
        print("❌ NVIDIA_API_KEY not found in environment.")
        return []

    from openai import OpenAI
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=api_key,
        timeout=REQUEST_TIMEOUT
    )

    models_to_test = [
        ("Primary", os.getenv("NVIDIA_MODEL_PRIMARY", "nvidia/nemotron-3.5-lightning-30b-a3b")),
        ("Secondary", os.getenv("NVIDIA_MODEL_SECONDARY", "meta/muse-glimmer-30b")),
        ("Tertiary", os.getenv("NVIDIA_MODEL_TERTIARY", "nvidia/nemotron-3.5-lightning-30b-a3b")),
    ]

    results = []
    for role, model_name in models_to_test:
        print(f"\n[NVIDIA NIM] Testing {role}: {model_name}...")
        start_time = time.time()
        
        extra_body = {}
        if "deepseek" in model_name.lower():
            extra_body = {"chat_template_kwargs": {"thinking": True}}
            
        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda m=model_name, eb=extra_body: client.chat.completions.create(
                    model=m,
                    messages=[{"role": "user", "content": TEST_PROMPT}],
                    max_tokens=60,
                    temperature=0.3,
                    extra_body=eb if eb else None
                )
            )
            elapsed = time.time() - start_time
            choice = response.choices[0]
            content = choice.message.content or getattr(choice.message, "reasoning_content", "") or ""
            content = content.strip().replace("\n", " ")
            print(f"  ✅ SUCCESS ({elapsed:.2f}s): {content[:80]}")
            results.append({"provider": "NVIDIA", "role": role, "model": model_name, "status": "PASS", "latency": f"{elapsed:.2f}s", "output": content[:60]})
        except Exception as err:
            elapsed = time.time() - start_time
            print(f"  ❌ FAILED ({elapsed:.2f}s): {type(err).__name__} - {err}")
            results.append({"provider": "NVIDIA", "role": role, "model": model_name, "status": "FAIL", "latency": f"{elapsed:.2f}s", "output": str(err)[:60]})

    return results


async def main():
    print("=" * 70)
    print(" 🧪 COUNCIL OF FRONTIERS - UNIFIED MODEL TEST SUITE")
    print(f" Loaded env: {ENV_PATH}")
    print(f" Prompt: \"{TEST_PROMPT}\"")
    print("=" * 70)

    groq_results = await test_groq_models()
    openrouter_results = await test_openrouter_models()
    nvidia_results = await test_nvidia_models()

    all_results = groq_results + openrouter_results + nvidia_results

    print("\n" + "=" * 70)
    print(" 📊 SUMMARY RESULTS")
    print("=" * 70)
    print(f"{'Provider':<12} | {'Role':<10} | {'Status':<6} | {'Latency':<8} | {'Model':<30}")
    print("-" * 70)
    for r in all_results:
        print(f"{r['provider']:<12} | {r['role']:<10} | {r['status']:<6} | {r['latency']:<8} | {r['model']:<30}")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
