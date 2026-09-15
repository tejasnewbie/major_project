"""Async LLM clients using official SDKs for Groq, Cerebras, and NVIDIA NIM."""
import asyncio
import time
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import httpx
from app.core.config import get_settings, Settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class LLMResponse:
    """Standardized response from any LLM provider."""
    content: str
    provider: str
    model: str
    latency: float
    tokens_used: Optional[int] = None
    error: Optional[str] = None


class RateLimiter:
    """Token bucket rate limiter."""
    
    def __init__(self, requests_per_minute: int):
        self.requests_per_minute = requests_per_minute
        self.interval = 60.0 / requests_per_minute
        self.last_request_time = 0
        self._lock = asyncio.Lock()
    
    async def acquire(self):
        """Wait until a request can be made."""
        async with self._lock:
            now = time.time()
            time_since_last = now - self.last_request_time
            if time_since_last < self.interval:
                wait_time = self.interval - time_since_last
                logger.debug(f"Rate limiting: waiting {wait_time:.2f}s")
                await asyncio.sleep(wait_time)
            self.last_request_time = time.time()


class BaseLLMClient(ABC):
    """Abstract base class for LLM clients."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.rate_limiter: Optional[RateLimiter] = None
    
    @abstractmethod
    async def generate(
        self, 
        model: str, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096
    ) -> LLMResponse:
        """Generate a completion from the LLM."""
        pass
    
    async def close(self):
        """Cleanup resources."""
        pass


class GroqClient(BaseLLMClient):
    """Client for Groq API using official SDK with multi-key pool rotation."""
    
    PER_KEY_TIMEOUT = 15.0

    def __init__(self, settings: Settings):
        super().__init__(settings)
        from groq import Groq
        self.api_keys = settings.get_groq_api_keys()
        if not self.api_keys and settings.groq_api_key:
            self.api_keys = [settings.groq_api_key.strip().strip('"\'')]
        self.current_key_idx = 0
        self.clients = [
            Groq(api_key=key, timeout=self.PER_KEY_TIMEOUT)
            for key in self.api_keys
        ]
        self.rate_limiter = RateLimiter(settings.groq_rate_limit)
    
    async def generate(
        self, 
        model: str, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096
    ) -> LLMResponse:
        """Generate completion using Groq SDK with automatic key rotation on error or 15s timeout."""
        start_time = time.time()
        # model is already a literal model ID — no settings lookup needed
        actual_model = model
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        total_keys = len(self.clients)
        if total_keys == 0:
            return LLMResponse(content="", provider="groq", model=actual_model, latency=0, error="No Groq API keys configured")

        last_error = None
        for attempt in range(total_keys):
            await self.rate_limiter.acquire()
            client = self.clients[self.current_key_idx]
            current_key_num = self.current_key_idx + 1
            call_start = time.time()

            try:
                logger.info(f"Groq request to {actual_model} (Key #{current_key_num}/{total_keys}, timeout={self.PER_KEY_TIMEOUT}s)...")
                loop = asyncio.get_event_loop()
                chat_completion = await asyncio.wait_for(
                    loop.run_in_executor(
                        None,
                        lambda c=client: c.chat.completions.create(
                            messages=messages,
                            model=actual_model,
                            temperature=temperature,
                            max_tokens=max_tokens
                        )
                    ),
                    timeout=self.PER_KEY_TIMEOUT
                )
                
                latency = time.time() - start_time
                content = chat_completion.choices[0].message.content or ""
                tokens = chat_completion.usage.total_tokens if chat_completion.usage else None
                
                logger.info(f"Groq response received in {latency:.1f}s (Key #{current_key_num})")
                
                return LLMResponse(
                    content=content,
                    provider="groq",
                    model=actual_model,
                    latency=latency,
                    tokens_used=tokens
                )
                
            except (asyncio.TimeoutError, TimeoutError) as e:
                call_elapsed = time.time() - call_start
                last_error = f"TimeoutError: Call exceeded {self.PER_KEY_TIMEOUT}s limit ({call_elapsed:.1f}s)"
                logger.warning(f"Groq Key #{current_key_num} exceeded {self.PER_KEY_TIMEOUT}s: rotating key...")
                if total_keys > 1 and attempt < total_keys - 1:
                    self.current_key_idx = (self.current_key_idx + 1) % total_keys
                    next_key_num = self.current_key_idx + 1
                    logger.info(f"Rotating Groq to Key #{next_key_num}/{total_keys}...")
                    await asyncio.sleep(0.1)
            except Exception as e:
                call_elapsed = time.time() - call_start
                last_error = f"{type(e).__name__}: {str(e)}"
                logger.warning(f"Groq Key #{current_key_num} error ({call_elapsed:.1f}s): {last_error}")
                if total_keys > 1 and attempt < total_keys - 1:
                    self.current_key_idx = (self.current_key_idx + 1) % total_keys
                    next_key_num = self.current_key_idx + 1
                    logger.info(f"Rotating Groq to Key #{next_key_num}/{total_keys}...")
                    await asyncio.sleep(0.1)

        return LLMResponse(
            content="",
            provider="groq",
            model=actual_model,
            latency=time.time() - start_time,
            error=f"All {total_keys} Groq key(s) failed. Last error: {last_error}"
        )


class OpenRouterClient(BaseLLMClient):
    """Client for OpenRouter API using OpenAI SDK with multi-key pool rotation."""
    
    PER_KEY_TIMEOUT = 15.0

    def __init__(self, settings: Settings):
        super().__init__(settings)
        from openai import OpenAI
        self.api_keys = settings.get_open_router_api_keys()
        if not self.api_keys and settings.open_router_api_key:
            self.api_keys = [settings.open_router_api_key.strip().strip('"\'')]
        self.current_key_idx = 0
        self.clients = [
            OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=key,
                timeout=self.PER_KEY_TIMEOUT
            )
            for key in self.api_keys
        ]
        self.rate_limiter = RateLimiter(settings.open_router_rate_limit)
    
    async def generate(
        self, 
        model: str, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096
    ) -> LLMResponse:
        """Generate completion using OpenRouter with automatic key rotation on error or 15s timeout."""
        start_time = time.time()
        # model is already a literal model ID — no settings lookup needed
        actual_model = model
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        total_keys = len(self.clients)
        if total_keys == 0:
            return LLMResponse(content="", provider="open_router", model=actual_model, latency=0, error="No OpenRouter API keys configured")

        last_error = None
        for attempt in range(total_keys):
            await self.rate_limiter.acquire()
            client = self.clients[self.current_key_idx]
            current_key_num = self.current_key_idx + 1
            call_start = time.time()

            try:
                logger.info(f"OpenRouter request to {actual_model} (Key #{current_key_num}/{total_keys}, timeout={self.PER_KEY_TIMEOUT}s)...")
                loop = asyncio.get_event_loop()
                chat_completion = await asyncio.wait_for(
                    loop.run_in_executor(
                        None,
                        lambda c=client: c.chat.completions.create(
                            messages=messages,
                            model=actual_model,
                            temperature=temperature,
                            max_tokens=max_tokens,
                            extra_headers={
                                "HTTP-Referer": "https://counciloffrontiers.local",
                                "X-Title": "Council of Frontiers"
                            }
                        )
                    ),
                    timeout=self.PER_KEY_TIMEOUT
                )
                
                latency = time.time() - start_time
                content = chat_completion.choices[0].message.content or ""
                tokens = chat_completion.usage.total_tokens if chat_completion.usage else None
                
                logger.info(f"OpenRouter response received in {latency:.1f}s (Key #{current_key_num})")
                
                return LLMResponse(
                    content=content,
                    provider="open_router",
                    model=actual_model,
                    latency=latency,
                    tokens_used=tokens
                )
                
            except (asyncio.TimeoutError, TimeoutError) as e:
                call_elapsed = time.time() - call_start
                last_error = f"TimeoutError: Call exceeded {self.PER_KEY_TIMEOUT}s limit ({call_elapsed:.1f}s)"
                logger.warning(f"OpenRouter Key #{current_key_num} exceeded {self.PER_KEY_TIMEOUT}s: rotating key...")
                if total_keys > 1 and attempt < total_keys - 1:
                    self.current_key_idx = (self.current_key_idx + 1) % total_keys
                    next_key_num = self.current_key_idx + 1
                    logger.info(f"Rotating OpenRouter to Key #{next_key_num}/{total_keys}...")
                    await asyncio.sleep(0.1)
            except Exception as e:
                call_elapsed = time.time() - call_start
                last_error = f"{type(e).__name__}: {str(e)}"
                logger.warning(f"OpenRouter Key #{current_key_num} error ({call_elapsed:.1f}s): {last_error}")
                if total_keys > 1 and attempt < total_keys - 1:
                    self.current_key_idx = (self.current_key_idx + 1) % total_keys
                    next_key_num = self.current_key_idx + 1
                    logger.info(f"Rotating OpenRouter to Key #{next_key_num}/{total_keys}...")
                    await asyncio.sleep(0.1)

        return LLMResponse(
            content="",
            provider="open_router",
            model=actual_model,
            latency=time.time() - start_time,
            error=f"All {total_keys} OpenRouter key(s) failed. Last error: {last_error}"
        )


class NvidiaClient(BaseLLMClient):
    """Client for NVIDIA NIM API using OpenAI SDK with multi-key pool rotation."""
    
    PER_KEY_TIMEOUT = 15.0

    def __init__(self, settings: Settings):
        super().__init__(settings)
        from openai import OpenAI
        self.api_keys = settings.get_nvidia_api_keys()
        if not self.api_keys and settings.nvidia_api_key:
            self.api_keys = [settings.nvidia_api_key.strip().strip('"\'')]
        self.current_key_idx = 0
        self.clients = [
            OpenAI(
                base_url="https://integrate.api.nvidia.com/v1",
                api_key=key,
                timeout=self.PER_KEY_TIMEOUT
            )
            for key in self.api_keys
        ]
        self.rate_limiter = RateLimiter(settings.nvidia_rate_limit)
    
    def _get_model_params(self, model: str) -> dict:
        """Get model-specific extra_body parameters."""
        if "deepseek" in model.lower():
            return {
                "chat_template_kwargs": {
                    "thinking": True
                }
            }
        return {}
    
    async def generate(
        self, 
        model: str, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096
    ) -> LLMResponse:
        """Generate completion using OpenAI SDK for NVIDIA NIM with key rotation on error or 15s timeout."""
        start_time = time.time()
        # model is already a literal model ID — no settings lookup needed
        actual_model = model
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        extra_body = self._get_model_params(actual_model)
        
        if "deepseek" in actual_model.lower():
            temperature = 0.2
            top_p = 0.7
        elif "kimi" in actual_model.lower() and "thinking" in actual_model.lower():
            temperature = 0.6
            top_p = 0.9
        else:
            top_p = 1.0
        
        total_keys = len(self.clients)
        if total_keys == 0:
            return LLMResponse(content="", provider="nvidia", model=actual_model, latency=0, error="No NVIDIA API keys configured")

        last_error = None
        for attempt in range(total_keys):
            await self.rate_limiter.acquire()
            client = self.clients[self.current_key_idx]
            current_key_num = self.current_key_idx + 1
            call_start = time.time()

            try:
                logger.info(f"NVIDIA request to {actual_model} (Key #{current_key_num}/{total_keys}, timeout={self.PER_KEY_TIMEOUT}s)...")
                loop = asyncio.get_event_loop()
                chat_completion = await asyncio.wait_for(
                    loop.run_in_executor(
                        None,
                        lambda c=client: c.chat.completions.create(
                            model=actual_model,
                            messages=messages,
                            temperature=temperature,
                            top_p=top_p,
                            max_tokens=max_tokens,
                            extra_body=extra_body
                        )
                    ),
                    timeout=self.PER_KEY_TIMEOUT
                )
                
                latency = time.time() - start_time
                content = ""
                reasoning_content = ""
                
                if chat_completion.choices and len(chat_completion.choices) > 0:
                    choice = chat_completion.choices[0]
                    if hasattr(choice, 'message') and choice.message:
                        content = choice.message.content or ""
                        reasoning = getattr(choice.message, 'reasoning_content', None)
                        if reasoning:
                            reasoning_content = reasoning
                            if "kimi" in actual_model.lower() and "thinking" in actual_model.lower():
                                if reasoning_content and content:
                                    content = f"<!-- Thinking -->\n{reasoning_content}\n\n<!-- Final Answer -->\n{content}"
                                elif reasoning_content:
                                    content = reasoning_content
                            elif content:
                                content = reasoning_content + "\n\n" + content
                            else:
                                content = reasoning_content
                        
                        if not content:
                            for attr in ['text', 'value', 'output']:
                                val = getattr(choice.message, attr, None)
                                if val:
                                    content = val
                                    break
                
                tokens = chat_completion.usage.total_tokens if chat_completion.usage else None
                logger.info(f"NVIDIA response received in {latency:.1f}s (Key #{current_key_num})")
                
                if not content:
                    raise ValueError("Empty response from model")
                
                return LLMResponse(
                    content=content,
                    provider="nvidia",
                    model=actual_model,
                    latency=latency,
                    tokens_used=tokens
                )
                
            except (asyncio.TimeoutError, TimeoutError) as e:
                call_elapsed = time.time() - call_start
                last_error = f"TimeoutError: Call exceeded {self.PER_KEY_TIMEOUT}s limit ({call_elapsed:.1f}s)"
                logger.warning(f"NVIDIA Key #{current_key_num} exceeded {self.PER_KEY_TIMEOUT}s: rotating key...")
                if total_keys > 1 and attempt < total_keys - 1:
                    self.current_key_idx = (self.current_key_idx + 1) % total_keys
                    next_key_num = self.current_key_idx + 1
                    logger.info(f"Rotating NVIDIA to Key #{next_key_num}/{total_keys}...")
                    await asyncio.sleep(0.1)
            except Exception as e:
                call_elapsed = time.time() - call_start
                last_error = f"{type(e).__name__}: {str(e)}"
                logger.warning(f"NVIDIA Key #{current_key_num} error ({call_elapsed:.1f}s): {last_error}")
                if total_keys > 1 and attempt < total_keys - 1:
                    self.current_key_idx = (self.current_key_idx + 1) % total_keys
                    next_key_num = self.current_key_idx + 1
                    logger.info(f"Rotating NVIDIA to Key #{next_key_num}/{total_keys}...")
                    await asyncio.sleep(0.1)

        return LLMResponse(
            content="",
            provider="nvidia",
            model=actual_model,
            latency=time.time() - start_time,
            error=f"All {total_keys} NVIDIA key(s) failed. Last error: {last_error}"
        )


class LLMClientManager:
    """Manager for multiple LLM clients with fallback support."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.clients: Dict[str, BaseLLMClient] = {}
        
        groq_keys = settings.get_groq_api_keys()
        if groq_keys:
            try:
                self.clients["groq"] = GroqClient(settings)
                logger.info(f"Groq client initialized with {len(groq_keys)} API key(s)")
            except Exception as e:
                logger.error(f"Failed to initialize Groq client: {e}")
        
        open_router_keys = settings.get_open_router_api_keys()
        if open_router_keys:
            try:
                self.clients["open_router"] = OpenRouterClient(settings)
                logger.info(f"OpenRouter client initialized with {len(open_router_keys)} API key(s)")
            except Exception as e:
                logger.error(f"Failed to initialize OpenRouter client: {e}")
        
        nvidia_keys = settings.get_nvidia_api_keys()
        if nvidia_keys:
            try:
                self.clients["nvidia"] = NvidiaClient(settings)
                logger.info(f"NVIDIA NIM client initialized with {len(nvidia_keys)} API key(s)")
            except Exception as e:
                logger.error(f"Failed to initialize NVIDIA client: {e}")
    
    async def generate_with_fallback(
        self,
        primary_provider: str,
        model: str,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096
    ) -> LLMResponse:
        """Generate with automatic fallback on failure."""
        # Priority order: primary -> others
        provider_order = [primary_provider] + [p for p in ["nvidia", "groq", "open_router"] if p != primary_provider]
        
        last_error = None
        for provider in provider_order:
            if provider not in self.clients:
                continue
            
            client = self.clients[provider]
            
            for attempt in range(self.settings.max_retries):
                try:
                    # Use appropriate model for each provider
                    actual_model = self._get_model_for_provider(provider, model)
                    
                    response = await client.generate(
                        model=actual_model,
                        prompt=prompt,
                        system_prompt=system_prompt,
                        temperature=temperature,
                        max_tokens=max_tokens
                    )
                    
                    if response.error is None:
                        return response
                    
                    last_error = response.error
                    logger.warning(f"{provider} attempt {attempt + 1} failed: {response.error}")
                    
                    if attempt < self.settings.max_retries - 1:
                        wait_time = self.settings.retry_delay * (2 ** attempt)
                        logger.info(f"Retrying in {wait_time}s...")
                        await asyncio.sleep(wait_time)
                        
                except Exception as e:
                    last_error = str(e)
                    logger.error(f"{provider} exception on attempt {attempt + 1}: {e}")
                    if attempt < self.settings.max_retries - 1:
                        wait_time = self.settings.retry_delay * (2 ** attempt)
                        await asyncio.sleep(wait_time)
        
        # All providers failed
        return LLMResponse(
            content="All LLM providers failed. Please check your API keys and rate limits.",
            provider="none",
            model="none",
            latency=0,
            error=f"All providers failed. Last error: {last_error}"
        )
    
    def _get_model_for_provider(self, provider: str, requested_model: str) -> str:
        """Return the model ID as-is — model names are already literal IDs in CATEGORY_MODEL_CONFIG."""
        return requested_model
    
    async def close_all(self):
        """Close all client connections."""
        for client in self.clients.values():
            await client.close()
