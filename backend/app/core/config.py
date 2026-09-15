"""Configuration management for Council of Frontiers."""
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List, Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Keys
    groq_api_key: str = ""
    groq_api_key2: str = ""
    groq_api_key3: str = ""
    groq_api_key4: str = ""
    groq_api_key5: str = ""

    open_router_api_key: str = ""
    open_router_api_key2: str = ""
    open_router_api_key3: str = ""
    open_router_api_key4: str = ""
    open_router_api_key5: str = ""

    nvidia_api_key: str = ""
    nvidia_api_key2: str = ""
    nvidia_api_key3: str = ""
    nvidia_api_key4: str = ""
    nvidia_api_key5: str = ""

    def get_groq_api_keys(self) -> List[str]:
        keys = [self.groq_api_key, self.groq_api_key2, self.groq_api_key3, self.groq_api_key4, self.groq_api_key5]
        import os
        for k, v in os.environ.items():
            if k.upper().startswith("GROQ_API_KEY") and v.strip() and v.strip() not in keys:
                keys.append(v.strip())
        return [k.strip().strip('"\'') for k in keys if k and k.strip().strip('"\'')]

    def get_nvidia_api_keys(self) -> List[str]:
        keys = [self.nvidia_api_key, self.nvidia_api_key2, self.nvidia_api_key3, self.nvidia_api_key4, self.nvidia_api_key5]
        import os
        for k, v in os.environ.items():
            if k.upper().startswith("NVIDIA_API_KEY") and v.strip() and v.strip() not in keys:
                keys.append(v.strip())
        return [k.strip().strip('"\'') for k in keys if k and k.strip().strip('"\'')]

    def get_open_router_api_keys(self) -> List[str]:
        keys = [self.open_router_api_key, self.open_router_api_key2, self.open_router_api_key3, self.open_router_api_key4, self.open_router_api_key5]
        import os
        for k, v in os.environ.items():
            if k.upper().startswith("OPEN_ROUTER_API_KEY") and v.strip() and v.strip() not in keys:
                keys.append(v.strip())
        return [k.strip().strip('"\'') for k in keys if k and k.strip().strip('"\'')]

    # =============================================
    # FAST MODEL CONFIGURATION (sub-1-minute target)
    # Primary: Groq (fastest inference available)
    # =============================================

    # GROQ — fastest inference, sub-3s per call
    groq_model_primary: str = "llama-3.3-70b-versatile"    # Fast + high quality
    groq_model_secondary: str = "llama-3.1-8b-instant"     # Ultra-fast
    groq_model_fallback: str = "gemma2-9b-it"              # Reliable backup

    # NVIDIA NIM — only fast nemotron models (NOT kimi/deepseek which are very slow)
    nvidia_model_primary: str = "nvidia/llama-3.3-nemotron-super-49b-v1"
    nvidia_model_secondary: str = "nvidia/llama-3.1-nemotron-70b-instruct"
    nvidia_model_tertiary: str = "nvidia/llama-3.3-nemotron-super-49b-v1"

    # OPEN ROUTER — fast free models only
    open_router_model_primary: str = "meta-llama/llama-3.3-70b-instruct:free"
    open_router_model_secondary: str = "meta-llama/llama-3.1-8b-instruct:free"
    open_router_model_fallback: str = "mistralai/mistral-7b-instruct:free"

    # Rate Limits
    groq_rate_limit: int = 30
    open_router_rate_limit: int = 20
    nvidia_rate_limit: int = 20

    # Retry Configuration
    max_retries: int = 2
    retry_delay: float = 1.0
    request_timeout: int = 30

    # Debate Configuration
    max_debate_rounds: int = 3
    similarity_threshold: float = 0.90
    enable_early_stopping: bool = True
    enable_iterative_refinement: bool = True
    enable_hierarchical_synthesis: bool = True

    # Code Execution
    docker_timeout: int = 30
    max_output_length: int = 10000
    debug: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


# =============================================
# MODEL ASSIGNMENTS — Groq-first for speed
# Using LITERAL model IDs (not settings attributes) so .env cannot override
# =============================================

CATEGORY_MODEL_CONFIG = {
    "design": {
        "generation": [
            {"provider": "groq", "model": "llama-3.3-70b-versatile", "reasoning_style": "creative"},
            {"provider": "groq", "model": "llama-3.1-8b-instant", "reasoning_style": "structured"},
            {"provider": "open_router", "model": "meta-llama/llama-3.3-70b-instruct:free", "reasoning_style": "visual"},
        ],
        "scoring": {"provider": "groq", "model": "llama-3.3-70b-versatile"},
        "refinement": [
            {"provider": "groq", "model": "llama-3.3-70b-versatile"},
            {"provider": "groq", "model": "gemma2-9b-it"},
        ],
        "synthesis": {"provider": "groq", "model": "llama-3.3-70b-versatile"},
    },
    "math": {
        "generation": [
            {"provider": "groq", "model": "llama-3.3-70b-versatile", "reasoning_style": "analytical"},
            {"provider": "groq", "model": "gemma2-9b-it", "reasoning_style": "step_by_step"},
            {"provider": "groq", "model": "llama-3.1-8b-instant", "reasoning_style": "rigorous"},
        ],
        "scoring": {"provider": "groq", "model": "llama-3.3-70b-versatile"},
        "refinement": [
            {"provider": "groq", "model": "llama-3.3-70b-versatile"},
            {"provider": "groq", "model": "llama-3.1-8b-instant"},
        ],
        "synthesis": {"provider": "groq", "model": "llama-3.3-70b-versatile"},
    },
    "code": {
        "generation": [
            {"provider": "groq", "model": "llama-3.3-70b-versatile", "reasoning_style": "optimal"},
            {"provider": "groq", "model": "gemma2-9b-it", "reasoning_style": "clean"},
            {"provider": "groq", "model": "llama-3.1-8b-instant", "reasoning_style": "robust"},
        ],
        "scoring": {"provider": "groq", "model": "llama-3.3-70b-versatile"},
        "refinement": [
            {"provider": "groq", "model": "llama-3.3-70b-versatile"},
            {"provider": "groq", "model": "llama-3.1-8b-instant"},
        ],
        "synthesis": {"provider": "groq", "model": "llama-3.3-70b-versatile"},
    },
    "factual": {
        "generation": [
            {"provider": "groq", "model": "llama-3.3-70b-versatile", "reasoning_style": "comprehensive"},
            {"provider": "groq", "model": "gemma2-9b-it", "reasoning_style": "concise"},
            {"provider": "groq", "model": "llama-3.1-8b-instant", "reasoning_style": "structured"},
        ],
        "scoring": {"provider": "groq", "model": "llama-3.3-70b-versatile"},
        "refinement": [
            {"provider": "groq", "model": "llama-3.3-70b-versatile"},
            {"provider": "groq", "model": "llama-3.1-8b-instant"},
        ],
        "synthesis": {"provider": "groq", "model": "llama-3.3-70b-versatile"},
    },
    "writing": {
        "generation": [
            {"provider": "groq", "model": "llama-3.3-70b-versatile", "reasoning_style": "engaging"},
            {"provider": "groq", "model": "gemma2-9b-it", "reasoning_style": "professional"},
            {"provider": "groq", "model": "llama-3.1-8b-instant", "reasoning_style": "creative"},
        ],
        "scoring": {"provider": "groq", "model": "llama-3.3-70b-versatile"},
        "refinement": [
            {"provider": "groq", "model": "llama-3.3-70b-versatile"},
            {"provider": "groq", "model": "llama-3.1-8b-instant"},
        ],
        "synthesis": {"provider": "groq", "model": "llama-3.3-70b-versatile"},
    },
    "general": {
        "generation": [
            {"provider": "groq", "model": "llama-3.3-70b-versatile", "reasoning_style": "analytical"},
            {"provider": "groq", "model": "gemma2-9b-it", "reasoning_style": "structured"},
            {"provider": "groq", "model": "llama-3.1-8b-instant", "reasoning_style": "balanced"},
        ],
        "scoring": {"provider": "groq", "model": "llama-3.3-70b-versatile"},
        "refinement": [
            {"provider": "groq", "model": "llama-3.3-70b-versatile"},
            {"provider": "groq", "model": "llama-3.1-8b-instant"},
        ],
        "synthesis": {"provider": "groq", "model": "llama-3.3-70b-versatile"},
    },
}



# Short, focused reasoning prompts (no lengthy multi-step instructions)
REASONING_PROMPTS = {
    "math": {
        "analytical": "Solve step-by-step. Show your work. State the final answer clearly.",
        "step_by_step": "Break down into clear numbered steps. State the final answer.",
        "rigorous": "Provide a rigorous solution with clear reasoning at each step.",
        "structured": "Show a structured solution with steps and a clear final answer.",
    },
    "code": {
        "optimal": "Write efficient, well-commented code that handles edge cases.",
        "clean": "Write clean, readable code with clear variable names.",
        "robust": "Write code with proper error handling.",
        "structured": "Write organized code with clear structure and comments.",
    },
    "design": {
        "creative": "Create an innovative, visually appealing implementation.",
        "structured": "Build a well-structured, maintainable implementation.",
        "visual": "Focus on visual quality and user experience.",
    },
    "factual": {
        "comprehensive": "Give a thorough, well-organized answer with key details.",
        "concise": "Give a clear, direct answer with the most important points.",
        "structured": "Present information clearly in logical sections.",
    },
    "writing": {
        "engaging": "Write compelling content that holds attention.",
        "professional": "Write polished, professional content.",
        "creative": "Write with creativity and distinct voice.",
        "structured": "Write organized content with clear flow.",
    },
    "general": {
        "analytical": "Analyze thoroughly and give a well-reasoned answer.",
        "structured": "Organize your answer clearly.",
        "balanced": "Consider multiple angles and give a balanced answer.",
    },
}

REFINEMENT_PROMPTS = {
    "system": "You are an expert improver. Improve the solution by fixing issues and enhancing quality. Output the COMPLETE improved solution.",
    "design": "Improve this design: fix errors, polish visuals, ensure all requirements are met.",
    "code": "Improve this code: fix bugs, add error handling, improve readability.",
    "math": "Improve this solution: fix errors, add missing steps, verify correctness.",
    "writing": "Improve this writing: fix grammar, strengthen arguments, improve flow.",
    "general": "Improve this solution: fix problems, add missing parts, enhance clarity.",
}

SYNTHESIS_STEP_PROMPTS = {
    "select": "Reply ONLY with the number of the best option (e.g. 1, 2, or 3).",
    "polish": "Provide the final, polished, production-ready version of this solution.",
}

CRITIQUE_SYSTEM_PROMPT = "Identify the top 3 issues with this solution: bugs, missing requirements, and improvements. Be brief and specific."

from functools import lru_cache
from typing import List, Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Keys (Supports single or multiple keys e.g. KEY, KEY2, KEY3, etc.)
    groq_api_key: str = ""
    groq_api_key2: str = ""
    groq_api_key3: str = ""
    groq_api_key4: str = ""
    groq_api_key5: str = ""

    open_router_api_key: str = ""
    open_router_api_key2: str = ""
    open_router_api_key3: str = ""
    open_router_api_key4: str = ""
    open_router_api_key5: str = ""

    nvidia_api_key: str = ""
    nvidia_api_key2: str = ""
    nvidia_api_key3: str = ""
    nvidia_api_key4: str = ""
    nvidia_api_key5: str = ""

    def get_groq_api_keys(self) -> List[str]:
        """Get all configured Groq API keys."""
        keys = [self.groq_api_key, self.groq_api_key2, self.groq_api_key3, self.groq_api_key4, self.groq_api_key5]
        import os
        for k, v in os.environ.items():
            if k.upper().startswith("GROQ_API_KEY") and v.strip() and v.strip() not in keys:
                keys.append(v.strip())
        return [k.strip().strip('"\'') for k in keys if k and k.strip().strip('"\'')]

    def get_nvidia_api_keys(self) -> List[str]:
        """Get all configured NVIDIA API keys."""
        keys = [self.nvidia_api_key, self.nvidia_api_key2, self.nvidia_api_key3, self.nvidia_api_key4, self.nvidia_api_key5]
        import os
        for k, v in os.environ.items():
            if k.upper().startswith("NVIDIA_API_KEY") and v.strip() and v.strip() not in keys:
                keys.append(v.strip())
        return [k.strip().strip('"\'') for k in keys if k and k.strip().strip('"\'')]

    def get_open_router_api_keys(self) -> List[str]:
        """Get all configured OpenRouter API keys."""
        keys = [self.open_router_api_key, self.open_router_api_key2, self.open_router_api_key3, self.open_router_api_key4, self.open_router_api_key5]
        import os
        for k, v in os.environ.items():
            if k.upper().startswith("OPEN_ROUTER_API_KEY") and v.strip() and v.strip() not in keys:
                keys.append(v.strip())
        return [k.strip().strip('"\'') for k in keys if k and k.strip().strip('"\'')]
    
    # ===========================================
    # MAXIMUM QUALITY MODEL CONFIGURATION
    # Based on: Kimi K2.5 (best synthesis), DeepSeek (best reasoning), 
    # GLM4.7 (best analysis), Groq/OpenRouter (speed)
    # ===========================================
    
    # --- NVIDIA NIM (Premium Quality - Slow but Best) ---
    # Kimi K2.5: Best for synthesis, reasoning, and final polish
    nvidia_model_primary: str = "moonshotai/kimi-k2-thinking"           # ⭐ BEST - Arbiter, Synthesis (with reasoning)
    nvidia_model_secondary: str = "deepseek-ai/deepseek-v3.1"    # Deep reasoning, math
    nvidia_model_tertiary: str = "z-ai/glm4.7"                   # Analysis, critique
    
    # --- GROQ (Fast & Capable) ---
    groq_model_primary: str = "meta-llama/llama-4-maverick-17b-128e-instruct"  # Fast generation
    groq_model_secondary: str = "openai/gpt-oss-120b"            # Diverse perspective
    groq_model_fallback: str = "llama-3.3-70b-versatile"         # Reliable backup
    
    # --- OPEN ROUTER ---
    open_router_model_primary: str = "liquid/lfm-2.5-2.6b:free"
    open_router_model_secondary: str = "nex-agi/nex-n2.5-mini:free"
    open_router_model_fallback: str = "cohere/north-mini-code:free"
    
    # Rate Limits (requests per minute)
    groq_rate_limit: int = 30
    open_router_rate_limit: int = 30
    nvidia_rate_limit: int = 30
    
    # Retry Configuration
    max_retries: int = 3
    retry_delay: float = 2.0
    request_timeout: int = 120  # Increased for Kimi K2.5
    
    # Debate Configuration
    max_debate_rounds: int = 4  # Now 4 rounds: Gen → Score → Refine → Synthesize
    similarity_threshold: float = 0.90
    enable_early_stopping: bool = True
    
    # Quality Settings
    enable_iterative_refinement: bool = True
    enable_hierarchical_synthesis: bool = True
    
    # Code Execution
    docker_timeout: int = 30
    max_output_length: int = 10000
    
    debug: bool = False
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
