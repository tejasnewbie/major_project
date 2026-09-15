# Council of Frontiers - Project Context

## Quick Summary
Multi-Agent Verification Framework using LLM Debate with 3 providers (Groq, Cerebras, NVIDIA NIM).

## Architecture
- **3-Round Process**: Generation → Critique → Synthesis
- **Category-Based Strategies**: Design, Math, Code, Factual, Writing, General
- **Auto-Scoring**: Solutions scored before critique
- **Token Management**: Automatic truncation to prevent limit errors

## Current Models
- **Groq**: moonshotai/kimi-k2-instruct, meta-llama/llama-4-maverick, openai/gpt-oss-120b
- **Cerebras**: llama-3.3-70b, llama-3.1-8b
- **NVIDIA**: deepseek-ai/deepseek-v3.1, z-ai/glm4.7

## Key Files
- `backend/app/core/strategies.py` - Category strategies
- `backend/app/services/debate_orchestrator.py` - Main debate logic
- `backend/app/core/config.py` - Model configuration

## Working Features
- Auto-problem classification
- Solution scoring & ranking
- Code execution sandbox
- Token limit handling

## Known Issues
- NVIDIA models slow (15-30s)
- Synthesis quality needs improvement
- Can hit rate limits on free tiers
