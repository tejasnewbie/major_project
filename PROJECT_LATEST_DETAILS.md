# Council of Frontiers - Project Latest Details

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Backend Details](#backend-details)
4. [Frontend Details](#frontend-details)
5. [Design System](#design-system)
6. [Features](#features)
7. [Configuration](#configuration)
8. [API Reference](#api-reference)
9. [File Structure](#file-structure)
10. [Models & Providers](#models--providers)
11. [Known Issues](#known-issues)

---

## Project Overview

**Council of Frontiers** is a Multi-Agent Verification Framework using LLM Debate. It's a Final Year Project (FYP) that orchestrates multiple free-tier LLMs to match or exceed paid flagship models through iterative debate, critique, and synthesis.

### Core Concept
Instead of using one expensive AI model, the system orchestrates multiple models to:
1. **Generate** solutions with divergent reasoning styles
2. **Evaluate & Score** each solution objectively
3. **Refine** the winning solution iteratively
4. **Synthesize** the best elements into a final answer

### Cost Analysis
| Approach | Monthly Cost | Latency | Quality |
|----------|-------------|---------|---------|
| Claude 3.5 Opus | $20 | Fast | 95% |
| GPT-4o | $20 | Fast | 94% |
| **Council of Frontiers** | **~$0-5** | **15-25s** | **Target: 95%+** |

---

## Architecture

### 4-Round Debate Process

```
┌─────────────────────────────────────────────────────────────┐
│                    USER QUERY                               │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  ROUND 0: CLASSIFICATION                                    │
│  └─ Auto-detect problem category (math, code, design, etc)  │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  ROUND 1: GENERATION (3 models in parallel)                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Agent 1    │  │   Agent 2    │  │   Agent 3    │      │
│  │  (NVIDIA)    │  │   (Groq)     │  │  (Cerebras)  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  ROUND 2: EVALUATION & SCORING                              │
│  ├─ Auto-score each solution (0-20)                         │
│  ├─ Code: Execute & test in Docker sandbox                  │
│  └─ Pick WINNER (highest score)                             │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  ROUND 3: REFINEMENT (Iterative)                            │
│  ├─ Generate critiques of winner                            │
│  ├─ Model D improves winner                                 │
│  └─ Model E improves winner again                           │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  ROUND 4: SYNTHESIS (Hierarchical)                          │
│  ├─ Select best from: original + 2 improvements             │
│  ├─ Final polish                                            │
│  └─ Output production-ready solution                        │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              FINAL ANSWER + CONFIDENCE SCORE                │
└─────────────────────────────────────────────────────────────┘
```

### Key Architectural Improvements
- **Iterative Refinement**: Models improve the winner rather than just critiquing
- **Hierarchical Synthesis**: Step-by-step selection instead of overwhelming arbiter
- **Category-Based Strategies**: Different models for different problem types
- **Token Management**: Automatic truncation to prevent API limits

---

## Backend Details

### Tech Stack
- **Framework**: FastAPI (Python 3.10+)
- **WebSocket**: Real-time streaming for frontend
- **Docker**: Isolated code execution sandbox
- **Rate Limiting**: Sequential API calls with exponential backoff

### Core Components

#### 1. Debate Orchestrator (`app/services/debate_orchestrator.py`)
- Main orchestration logic
- 4-round debate process implementation
- Progress streaming via WebSocket
- Handles agent responses and result aggregation

**Key Classes:**
- `AgentResponse`: Response from a single agent
- `DebateResult`: Complete debate result with all metadata
- `DebateOrchestrator`: Main orchestrator class

#### 2. Strategies (`app/core/strategies.py`)
- Category-based strategies for different problem types
- Auto-scoring based on category criteria
- Iterative refinement prompts
- Token management and truncation

**Categories:**
- `DesignStrategy`: Auto-scoring on creativity, functionality, code quality
- `MathStrategy`: Consensus detection + correctness verification
- `CodeStrategy`: Execution testing + bug detection
- `FactualStrategy`: Completeness + structure scoring
- `WritingStrategy`: Style + clarity scoring
- `GeneralStrategy`: Balanced approach

#### 3. LLM Client (`app/services/llm_client.py`)
- Multi-provider client (Groq, Cerebras, NVIDIA)
- Rate limiting and retry logic
- Fallback mechanism between providers
- Unified response format

**Supported Providers:**
- **GroqClient**: Official groq SDK (8k token limit)
- **CerebrasClient**: Official cerebras-cloud-sdk (16k token limit)
- **NvidiaClient**: OpenAI SDK with NVIDIA base URL (16k token limit)

#### 4. Problem Classifier (`app/core/classifier.py`)
- Auto-classifies queries into categories
- Uses keyword matching and heuristics
- Categories: design, math, code, factual, writing, general

#### 5. Code Executor (`app/services/code_executor.py`)
- Docker-based code execution
- Isolated sandbox environment
- Security: Non-root user, read-only filesystem, network isolation
- Memory limit: 512MB, CPU limit: 0.5 cores, Timeout: 30s

### Environment Variables (`.env`)
```bash
# API Keys
GROQ_API_KEY=your_key
CEREBRAS_API_KEY=your_key
NVIDIA_API_KEY=your_key

# Groq Models
GROQ_MODEL_PRIMARY=meta-llama/llama-4-maverick
GROQ_MODEL_SECONDARY=openai/gpt-oss-120b
GROQ_MODEL_FALLBACK=llama-3.3-70b-versatile

# Cerebras Models
CEREBRAS_MODEL_PRIMARY=llama-3.3-70b
CEREBRAS_MODEL_SECONDARY=llama-3.1-8b

# NVIDIA Models
NVIDIA_MODEL_PRIMARY=moonshotai/kimi-k2-thinking
NVIDIA_MODEL_SECONDARY=deepseek-ai/deepseek-v3.1
NVIDIA_MODEL_TERTIARY=z-ai/glm4.7

# Rate Limits (requests per minute)
GROQ_RATE_LIMIT=20
CEREBRAS_RATE_LIMIT=10
NVIDIA_RATE_LIMIT=20

# Features
ENABLE_EARLY_STOPPING=true
SIMILARITY_THRESHOLD=0.90
```

---

## Frontend Details

### Tech Stack
- **Framework**: React 18
- **Build Tool**: Create React App
- **Styling**: CSS Variables + Custom CSS
- **WebSocket**: Native WebSocket API
- **Background**: CSS animations (GPU-accelerated)

### Component Structure

#### 1. App.jsx
- Main application component
- WebSocket connection management
- State management for debate flow
- Progress tracking

#### 2. QueryInput Component
- User input textarea
- Auto-expanding
- Glassmorphism effect (transparent → blur on focus)
- Submit button with loading state

#### 3. ThinkingBar Component
- Animated progress indicator
- Shows current stage (Generation, Evaluation, Refinement, Synthesis)
- Agent dots showing which models are active
- Progress bar with shimmer effect

#### 4. CollapsibleRound Component
- Round 1 (Generation) and Round 2 (Refinement) cards
- Expandable to show agent details
- Status indicators (Done, Active, Pending)
- Agent pills showing model progress

#### 5. FinalAnswer Component
- Displays final synthesized answer
- Quality score badge
- Copy button
- Collapsible thinking process section
- Code block support

#### 6. CodeBlock Component
- GitHub Dark theme syntax highlighting
- Line numbers
- Copy button with feedback
- Download button
- Supports filename display

#### 7. OptimizedBackground Component
- CSS-only animated background
- 3 floating gradient blobs
- GPU-accelerated animations
- Noise texture overlay
- Vignette effect

### Design System

#### Color Palette (Teal Theme)
```css
/* Core */
--bg-primary: #0a0f0f;
--bg-secondary: #0f1414;
--bg-tertiary: #141a1a;
--bg-elevated: #1a2020;

/* Text */
--text-primary: #e0f2f1;
--text-secondary: #94a3a3;
--text-tertiary: #647474;

/* Accent (Teal) */
--accent: #0d8a8a;
--accent-hover: #10a0a0;
--accent-light: #14b8b8;
--accent-glow: rgba(13, 138, 138, 0.25);

/* Borders */
--border: #1a2626;
--border-hover: #263535;
```

#### Typography
- **Font Family**: Inter (sans-serif), JetBrains Mono (monospace)
- **Base Size**: 15px
- **Line Height**: 1.6

#### Spacing System
```
--space-xs: 4px
--space-sm: 8px
--space-md: 16px
--space-lg: 24px
--space-xl: 32px
```

---

## Features

### 1. Multi-Provider Support
- Groq (20 req/min free)
- Cerebras (10 req/min free)
- NVIDIA NIM (varies by model)

### 2. Category-Based Reasoning
Different reasoning styles based on problem type:
- **Math**: Analytical, Intuitive, Structured
- **Code**: Optimal, Clean, Robust
- **Design**: Creative, Structured, Visual
- **Writing**: Engaging, Professional, Creative

### 3. Execution-Augmented Debate
For coding tasks:
- Code extracted from each solution
- Executed in isolated Docker container
- Error traces fed back into critique round
- Only working solutions advance

### 4. Token Management
- Automatic truncation when passing content between models
- Provider-specific limits (Groq 8k, Cerebras/NVIDIA 16k)
- Prevents API limit errors

### 5. Early Stopping
- If 3 models agree >90% (TF-IDF similarity), skip to synthesis
- Saves time and API calls

### 6. Rate Limit Handling
- Sequential API calls to respect limits
- Exponential backoff on failures
- Automatic fallback between providers

---

## Configuration

### Backend Configuration
All configuration is in `backend/.env`:

**Required:**
- `GROQ_API_KEY` - From console.groq.com
- `CEREBRAS_API_KEY` - From cloud.cerebras.ai
- `NVIDIA_API_KEY` - From build.nvidia.com

**Optional:**
- Model selection (defaults provided)
- Rate limits (defaults match free tiers)
- Feature flags (early stopping, similarity threshold)

### Frontend Configuration
Frontend connects to backend via WebSocket at `ws://localhost:8000/api/ws/debate`

Proxy configuration in `frontend/package.json`:
```json
"proxy": "http://localhost:8000"
```

---

## API Reference

### REST Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/config` | GET | Current configuration |
| `/api/debate` | POST | Run debate (sync) |
| `/api/execute` | POST | Test code execution |
| `/api/examples` | GET | Example queries |

### WebSocket Endpoint

| Endpoint | Description |
|----------|-------------|
| `/api/ws/debate` | Real-time streaming debate |

**WebSocket Message Format:**
```json
{
  "type": "progress",
  "stage": "round1_start",
  "message": "Generation: Creating solutions...",
  "data": {},
  "timestamp": "2024-01-01T00:00:00"
}
```

**Complete Message:**
```json
{
  "type": "complete",
  "result": {
    "query": "...",
    "category": "code",
    "final_answer": "...",
    "confidence": 0.85,
    "latency": 45.2,
    "round1": [...],
    "refinements": [...]
  }
}
```

---

## File Structure

```
council-of-frontiers/
├── README.md                          # Main readme
├── ARCHITECTURE_v2.md                 # Architecture documentation
├── PROJECT_CONTEXT.md                 # Quick reference
├── PROJECT_LATEST_DETAILS.md          # This file
├── SETUP_GUIDE.md                     # Setup instructions
├── IMPLEMENTATION_GUIDE.md            # Implementation details
├── setup.py                           # Python package setup
├── start.bat                          # Windows startup script
├── start.sh                           # Unix startup script
│
├── backend/
│   ├── .env                           # Environment variables (create from .env.example)
│   ├── .env.example                   # Environment template
│   ├── requirements.txt               # Python dependencies
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI entry point
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes.py              # API endpoints (REST + WebSocket)
│   │   │
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── classifier.py          # Problem classification
│   │   │   ├── config.py              # Settings & model config
│   │   │   └── strategies.py          # Category strategies
│   │   │
│   │   ├── models/
│   │   │   └── __init__.py
│   │   │
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── code_executor.py       # Docker code execution
│   │       ├── debate_orchestrator.py # Main debate logic
│   │       └── llm_client.py          # Multi-provider LLM clients
│   │
│   └── docker-sandbox/
│       ├── Dockerfile                 # Code execution container
│       ├── docker-compose.yml
│       └── .dockerignore
│
├── frontend/
│   ├── package.json                   # Node dependencies
│   ├── package-lock.json
│   │
│   ├── public/
│   │   └── index.html                 # HTML entry point
│   │
│   └── src/
│       ├── index.js                   # React entry point
│       ├── index.css                  # Global styles
│       ├── App.jsx                    # Main app component
│       ├── App.css                    # App styles
│       │
│       ├── components/
│       │   ├── AgentBubble.jsx        # Model response display (legacy)
│       │   ├── AgentBubble.css
│       │   ├── CodeBlock.jsx          # Code display with syntax highlighting
│       │   ├── CodeBlock.css
│       │   ├── CollapsibleRound.jsx   # Expandable round cards
│       │   ├── CollapsibleRound.css
│       │   ├── FinalAnswer.jsx        # Final answer display
│       │   ├── FinalAnswer.css
│       │   ├── OptimizedBackground.jsx # CSS background
│       │   ├── OptimizedBackground.css
│       │   ├── ProgressBar.jsx        # Progress indicator (legacy)
│       │   ├── ProgressBar.css
│       │   ├── QueryInput.jsx         # User input component
│       │   ├── QueryInput.css
│       │   ├── ThinkingBar.jsx        # Thinking progress bar
│       │   ├── ThinkingBar.css
│       │   ├── ShaderAnimation.jsx    # Three.js background (legacy)
│       │   └── ShaderAnimation.css
│       │
│       ├── hooks/
│       │   └── useWebSocket.js        # WebSocket hook
│       │
│       └── styles/
│           ├── variables.css          # CSS variables (design system)
│           └── aether-design-system.css # Additional styles
│
└── docker-sandbox/                    # Code execution environment
    ├── Dockerfile
    ├── docker-compose.yml
    └── .dockerignore
```

---

## Models & Providers

### Current Model Assignments

#### Groq (20 req/min free)
- `meta-llama/llama-4-maverick` - Primary (fast, versatile)
- `openai/gpt-oss-120b` - Secondary (reasoning)
- `llama-3.3-70b-versatile` - Fallback (reliable)

#### Cerebras (10 req/min free)
- `llama-3.3-70b` - Primary (high quality)
- `llama-3.1-8b` - Secondary (fast)

#### NVIDIA NIM (varies)
- `moonshotai/kimi-k2-thinking` - Synthesis & refinement (best reasoning)
- `deepseek-ai/deepseek-v3.1` - Math & logic
- `z-ai/glm4.7` - Critique & analysis

### Model Roles by Category

| Category | Generation | Scoring | Refinement | Synthesis |
|----------|------------|---------|------------|-----------|
| **Design** | DeepSeek, Llama 4, Cerebras | GLM4.7 | Kimi K2.5, Llama 3.3 | **Kimi K2.5** |
| **Math** | DeepSeek, Llama 3.3, Cerebras | DeepSeek | DeepSeek, GLM4.7 | **DeepSeek** |
| **Code** | DeepSeek, Llama 4, Cerebras | GLM4.7 | Kimi K2.5, Llama 3.3 | **Kimi K2.5** |
| **Writing** | Kimi K2.5, GPT-OSS, Cerebras | Kimi K2.5 | Kimi K2.5, GLM4.7 | **Kimi K2.5** |

---

## Known Issues

### 1. Performance
- **Issue**: Website felt laggy with Three.js shader background
- **Solution**: Replaced with CSS-only optimized background using GPU-accelerated animations

### 2. API Limits
- **Issue**: Can hit rate limits on free tiers during high usage
- **Solution**: Sequential API calls with exponential backoff and fallback mechanism

### 3. NVIDIA Models Slow
- **Issue**: NVIDIA NIM models take 15-30s per request
- **Mitigation**: Used for synthesis/refinement only, not generation

### 4. Cache Issues
- **Issue**: Browser caching old CSS/JS after updates
- **Solution**: Hard refresh (Ctrl+Shift+R) or cache-busting meta tags in index.html

### 5. WebSocket Connection
- **Issue**: Proxy errors when backend not running
- **Solution**: Ensure backend is started before frontend

---

## Development Tips

### Starting the Project
```bash
# Terminal 1: Backend
cd backend
uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm start
```

### Testing Debate
```bash
curl -X POST "http://localhost:8000/api/debate" \
  -H "Content-Type: application/json" \
  -d '{"query": "Calculate the 10th Fibonacci number"}'
```

### Testing Code Execution
```bash
curl -X POST "http://localhost:8000/api/execute" \
  -H "Content-Type: application/json" \
  -d '{"code": "print(sum(range(10)))"}'
```

---

## Future Enhancements

1. **Performance Mode Toggle**: Allow users to switch between quality and speed
2. **Conversation History**: Persist debates to database
3. **Export Options**: PDF, Markdown export for results
4. **Custom Models**: Allow users to add their own API keys for other providers
5. **Mobile App**: React Native version

---

## License

MIT License - Academic Use

Built for Final Year Project CSE 2024
