"""Configuration management for Council of Frontiers - Maximum Quality Setup."""
from pydantic_settings import BaseSettings
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


# ===========================================
# OPTIMIZED MODEL ASSIGNMENTS BY CATEGORY
# ===========================================
# Strategy: Use best model for each specific task

CATEGORY_MODEL_CONFIG = {
    "design": {
        "generation": [
            {"provider": "nvidia", "model": "nvidia_model_secondary", "reasoning_style": "creative"},  # DeepSeek creative
            {"provider": "groq", "model": "groq_model_primary", "reasoning_style": "structured"},      # Fast implementation
            {"provider": "open_router", "model": "open_router_model_primary", "reasoning_style": "visual"},  # Visual design
        ],
        "scoring": {"provider": "nvidia", "model": "nvidia_model_tertiary"},  # GLM4.7 scores design
        "refinement": [
            {"provider": "nvidia", "model": "nvidia_model_primary"},   # Kimi K2 Thinking improves design
            {"provider": "groq", "model": "groq_model_fallback"},     # Fast polish
        ],
        "synthesis": {"provider": "nvidia", "model": "nvidia_model_primary"},  # Kimi K2 Thinking final
    },
    
    "math": {
        "generation": [
            {"provider": "nvidia", "model": "nvidia_model_secondary", "reasoning_style": "analytical"},  # DeepSeek math
            {"provider": "groq", "model": "groq_model_fallback", "reasoning_style": "step_by_step"},    # Clear steps
            {"provider": "open_router", "model": "open_router_model_primary", "reasoning_style": "rigorous"}, # Formal proof
        ],
        "scoring": {"provider": "nvidia", "model": "nvidia_model_secondary"},  # DeepSeek checks math
        "refinement": [
            {"provider": "nvidia", "model": "nvidia_model_secondary"},  # DeepSeek improves proof
            {"provider": "nvidia", "model": "nvidia_model_tertiary"},   # GLM4.7 checks logic
        ],
        "synthesis": {"provider": "nvidia", "model": "nvidia_model_secondary"},  # DeepSeek final
    },
    
    "code": {
        "generation": [
            {"provider": "nvidia", "model": "nvidia_model_secondary", "reasoning_style": "optimal"},    # DeepSeek code
            {"provider": "groq", "model": "groq_model_primary", "reasoning_style": "clean"},           # Clean implementation
            {"provider": "open_router", "model": "open_router_model_primary", "reasoning_style": "robust"},  # Error handling
        ],
        "scoring": {"provider": "nvidia", "model": "nvidia_model_tertiary"},  # GLM4.7 scores code
        "refinement": [
            {"provider": "nvidia", "model": "nvidia_model_primary"},   # Kimi K2 Thinking improves code
            {"provider": "groq", "model": "groq_model_fallback"},     # Fast optimization
        ],
        "synthesis": {"provider": "nvidia", "model": "nvidia_model_primary"},  # Kimi K2 Thinking final code
    },
    
    "factual": {
        "generation": [
            {"provider": "nvidia", "model": "nvidia_model_tertiary", "reasoning_style": "comprehensive"},  # GLM4.7 thorough
            {"provider": "groq", "model": "groq_model_secondary", "reasoning_style": "concise"},          # GPT-OSS concise
            {"provider": "open_router", "model": "open_router_model_primary", "reasoning_style": "structured"}, # Organized
        ],
        "scoring": {"provider": "nvidia", "model": "nvidia_model_primary"},  # Kimi K2 Thinking evaluates
        "refinement": [
            {"provider": "nvidia", "model": "nvidia_model_tertiary"},   # GLM4.7 adds detail
            {"provider": "groq", "model": "groq_model_fallback"},       # Clarify
        ],
        "synthesis": {"provider": "nvidia", "model": "nvidia_model_primary"},  # Kimi K2 Thinking final
    },
    
    "writing": {
        "generation": [
            {"provider": "nvidia", "model": "nvidia_model_primary", "reasoning_style": "engaging"},    # Kimi K2 Thinking engaging
            {"provider": "groq", "model": "groq_model_secondary", "reasoning_style": "professional"}, # GPT-OSS formal
            {"provider": "open_router", "model": "open_router_model_primary", "reasoning_style": "creative"}, # Creative
        ],
        "scoring": {"provider": "nvidia", "model": "nvidia_model_primary"},  # Kimi K2 Thinking scores writing
        "refinement": [
            {"provider": "nvidia", "model": "nvidia_model_primary"},   # Kimi K2 Thinking improves prose
            {"provider": "nvidia", "model": "nvidia_model_tertiary"},  # GLM4.7 checks clarity
        ],
        "synthesis": {"provider": "nvidia", "model": "nvidia_model_primary"},  # Kimi K2 Thinking final polish
    },
    
    "general": {
        "generation": [
            {"provider": "nvidia", "model": "nvidia_model_secondary", "reasoning_style": "analytical"},
            {"provider": "groq", "model": "groq_model_primary", "reasoning_style": "structured"},
            {"provider": "open_router", "model": "open_router_model_primary", "reasoning_style": "balanced"},
        ],
        "scoring": {"provider": "nvidia", "model": "nvidia_model_tertiary"},
        "refinement": [
            {"provider": "nvidia", "model": "nvidia_model_primary"},
            {"provider": "groq", "model": "groq_model_fallback"},
        ],
        "synthesis": {"provider": "nvidia", "model": "nvidia_model_primary"},
    }
}


# ===========================================
# ENHANCED REASONING PROMPTS
# ===========================================

REASONING_PROMPTS = {
    "math": {
        "analytical": """Solve this rigorously using formal mathematical methods:
1. State all given information clearly
2. Identify the appropriate theorem/technique
3. Show every step with justification
4. Verify each step is correct
5. State final answer clearly
6. Check answer by substitution or alternative method""",
        
        "step_by_step": """Break down the solution methodically:
1. What are we trying to find?
2. What do we know?
3. What formula/theorem applies?
4. Execute calculations showing work
5. Verify the answer makes sense""",
        
        "rigorous": """Provide a formal mathematical proof:
- State assumptions explicitly
- Use proper mathematical notation
- Each step must follow logically
- Consider all edge cases
- Conclude with Q.E.D. or equivalent""",
        
        "structured": """Present mathematical solution clearly:
- State the problem
- Show step-by-step working
- Explain reasoning at each step
- State final answer clearly
- Verify correctness""",
    },
    
    "code": {
        "optimal": """Write optimal, production-ready code:
1. Analyze time/space complexity requirements
2. Choose the most efficient algorithm
3. Implement with clean, readable code
4. Handle all edge cases
5. Add comprehensive error handling
6. Include comments explaining key logic
7. Verify with example usage""",
        
        "clean": """Write clean, maintainable code:
- Use descriptive variable names
- Keep functions focused and small
- Follow language best practices
- Add docstrings/comments
- Handle errors gracefully
- Make it easy to understand and modify""",
        
        "robust": """Write robust, bulletproof code:
- Validate all inputs
- Handle edge cases explicitly
- Use try-catch for error handling
- Include input sanitization
- Add logging for debugging
- Ensure it never crashes unexpectedly""",
        
        "structured": """Write well-structured code:
- Clear function/class organization
- Logical code flow
- Appropriate comments
- Proper error handling
- Easy to read and maintain""",
    },
    
    "design": {
        "creative": """Create an innovative, visually striking design:
1. Analyze requirements thoroughly
2. Brainstorm creative approaches
3. Choose most unique/impressive concept
4. Implement with attention to visual details
5. Ensure responsive/adaptive behavior
6. Add subtle animations/interactions
7. Make it memorable and polished""",
        
        "structured": """Build a well-structured, maintainable implementation:
- Semantic HTML structure
- Organized CSS (BEM or similar)
- Modular component approach
- Clean separation of concerns
- Easy to customize and extend""",
        
        "visual": """Focus on visual excellence:
- Beautiful color palette
- Thoughtful typography
- Proper spacing and alignment
- Visual hierarchy
- Attention to micro-interactions
- Professional polish""",
    },
    
    "factual": {
        "comprehensive": """Provide a thorough, well-researched answer:
1. Cover all aspects of the question
2. Provide specific examples and evidence
3. Explain underlying mechanisms/principles
4. Address common misconceptions
5. Cite relevant facts/data
6. Structure logically with clear headings""",
        
        "concise": """Give a clear, direct answer:
- Main point first
- Key supporting facts
- Brief examples
- No unnecessary elaboration
- Easy to scan and understand""",
        
        "structured": """Present information in organized format:
- Overview/summary first
- Break into logical sections
- Use bullet points for lists
- Include specific details
- End with key takeaways""",
    },
    
    "writing": {
        "engaging": """Write compelling, engaging content:
1. Hook the reader immediately
2. Maintain interest throughout
3. Use vivid language and examples
4. Vary sentence structure
5. Build to a satisfying conclusion
6. Make the reader feel something""",
        
        "professional": """Write polished, professional content:
- Appropriate tone for context
- Clear, error-free writing
- Logical flow of ideas
- Professional vocabulary
- Proper formatting
- Ready for publication""",
        
        "creative": """Write with creativity and flair:
- Unique perspective or angle
- Creative word choice
- Engaging narrative flow
- Memorable phrases
- Distinct voice""",
        
        "structured": """Write well-organized content:
- Clear introduction
- Logical paragraph structure
- Smooth transitions
- Strong conclusion
- Easy to follow and understand""",
    },
    
    "general": {
        "analytical": "Analyze thoroughly, considering all perspectives and implications.",
        "structured": "Organize clearly with logical flow and distinct sections.",
        "balanced": "Present a balanced view considering multiple angles.",
    }
}


# Iterative refinement prompts
REFINEMENT_PROMPTS = {
    "system": """You are an expert improver. Your task is to take the BEST solution and make it even better.

Focus on:
1. Fixing bugs/errors identified in critiques
2. Adding missing features/requirements
3. Improving clarity and readability
4. Enhancing efficiency where possible
5. Maintaining what already works well

Output the COMPLETE improved solution.""",

    "design": """Improve this design solution:
- Fix any HTML/CSS errors
- Ensure all requirements are met
- Improve visual polish
- Add missing interactions
- Optimize performance
- Make it production-ready""",

    "code": """Improve this code:
- Fix bugs from critiques
- Add missing error handling
- Improve efficiency
- Enhance readability
- Ensure it passes all test cases
- Add helpful comments""",

    "math": """Improve this mathematical solution:
- Fix any calculation errors
- Strengthen the proof
- Add missing steps
- Clarify explanations
- Verify correctness
- Make it elegant""",

    "writing": """Improve this writing:
- Fix grammar and style issues
- Strengthen arguments
- Improve flow
- Enhance engagement
- Polish language
- Perfect the tone""",

    "general": """Improve this solution:
- Address all criticisms
- Fix identified problems
- Add missing elements
- Enhance clarity
- Make it comprehensive""",
}


# Hierarchical synthesis prompts (step by step)
SYNTHESIS_STEP_PROMPTS = {
    "select": """Select the single best solution based on:
1. Correctness (most important)
2. Completeness (all requirements met)
3. Quality (best implementation)

Do NOT combine solutions. Pick ONE winner.

Respond with:
- Selected solution number
- Why it's the best
- Key strengths""",

    "apply_fixes": """Apply improvements to the selected solution:
- Fix bugs from critiques
- Add missing features
- Address weaknesses mentioned
- Keep what works well

Output the improved solution.""",

    "polish": """Final polish:
- Perfect formatting
- Ensure completeness
- Check requirements
- Professional presentation

Output the FINAL, PRODUCTION-READY solution.""",
}


# Enhanced critique prompt for finding bugs
CRITIQUE_SYSTEM_PROMPT = """You are an expert reviewer focused on finding issues. Be thorough and specific.

For each solution, identify:
1. BUGS: Specific errors that break functionality
2. MISSING: Requirements not met
3. IMPROVEMENTS: Ways to make it better
4. EDGE CASES: Scenarios not handled

Format your critique as:
- Issue: [specific problem]
- Location: [where in the code/solution]
- Fix: [how to correct it]

Be constructive but honest."""
