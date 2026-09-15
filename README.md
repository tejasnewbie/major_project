# Council of Frontiers 🏛️

**Multi-Agent Verification Framework using LLM Debate**

A Final Year Project that orchestrates multiple free-tier LLMs (Groq + Cerebras) to match or exceed paid flagship models through iterative debate, critique, and synthesis.

## 🎯 Core Concept

Instead of using one expensive AI, we orchestrate 3 models to:
1. **Generate** solutions with divergent reasoning styles
2. **Critique** each other's solutions
3. **Synthesize** the best elements into a final answer

Like putting smart experts in a room who check each other's work before finalizing.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER QUERY                               │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  ROUND 1: GENERATION (Parallel with Rate Limiting)          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Agent 1    │  │   Agent 2    │  │   Agent 3    │      │
│  │   (Groq)     │  │ (Cerebras)   │  │   (Groq)     │      │
│  │  Analytical  │  │  Intuitive   │  │  Structured  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└──────────────────────┬──────────────────────────────────────┘
                       │
           ┌───────────┴───────────┐
           │  Similarity Check     │
           │  >90%? Early Stop     │
           └───────────┬───────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  ROUND 2: CRITIQUE (Each reviews the other two)             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Critic 1   │  │   Critic 2   │  │   Critic 3   │      │
│  │ (Cerebras)   │  │   (Groq)     │  │ (Cerebras)   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  ROUND 3: SYNTHESIS (Arbiter)                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Groq (Strongest Model)                 │   │
│  │         Combines best + Outputs confidence          │   │
│  └─────────────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              FINAL ANSWER + CONFIDENCE SCORE                │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- Docker Desktop (for code execution sandbox)
- API keys from:
  - [Groq](https://console.groq.com/) (free tier: 20 req/min)
  - [Cerebras](https://cloud.cerebras.ai/) (free tier: 10 req/min)

### 1. Clone and Setup

```bash
cd council-of-frontiers

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install
```

### 2. Configure Environment

```bash
cd backend
cp .env.example .env
# Edit .env with your API keys:
# GROQ_API_KEY=your_key_here
# CEREBRAS_API_KEY=your_key_here
```

### 3. Start Services

```bash
# Terminal 1: Backend
cd backend
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm start
```

Visit `http://localhost:3000`

## 📁 Project Structure

```
council-of-frontiers/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py           # FastAPI endpoints
│   │   ├── core/
│   │   │   └── config.py           # Settings & model config
│   │   ├── services/
│   │   │   ├── llm_client.py       # Groq + Cerebras clients
│   │   │   ├── debate_orchestrator.py  # Core debate logic
│   │   │   └── code_executor.py    # Docker sandbox
│   │   └── main.py                 # FastAPI app
│   ├── docker-sandbox/             # Code execution container
│   ├── .env.example
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AgentBubble.jsx     # Model response display
│   │   │   ├── FinalAnswer.jsx     # Synthesis display
│   │   │   ├── ProgressBar.jsx     # Stage indicator
│   │   │   └── QueryInput.jsx      # User input
│   │   ├── hooks/
│   │   │   └── useWebSocket.js     # Real-time connection
│   │   └── App.jsx
│   └── package.json
└── README.md
```

## 🔧 Configuration

Edit `backend/.env` to customize:

```bash
# API Keys
GROQ_API_KEY=your_key
CEREBRAS_API_KEY=your_key

# Models (Groq)
GROQ_MODEL_PRIMARY=llama-3.3-70b-versatile
GROQ_MODEL_SECONDARY=llama-3.1-8b-instant
GROQ_MODEL_FALLBACK=mixtral-8x7b-32768

# Models (Cerebras)
CEREBRAS_MODEL_PRIMARY=llama3.3-70b
CEREBRAS_MODEL_SECONDARY=llama3.1-8b

# Rate Limits
GROQ_RATE_LIMIT=20
CEREBRAS_RATE_LIMIT=10

# Features
ENABLE_EARLY_STOPPING=true
SIMILARITY_THRESHOLD=0.90
```

## 🔬 How It Works

### Dynamic Reasoning
Based on problem type, models use different approaches:
- **Math**: Analytical (step-by-step), Intuitive (pattern), Structured (algorithm)
- **Code**: Efficiency focus, Readability focus, Systematic approach
- **Logic**: Formal logic, Analogy-based, Structured deduction

### Execution-Augmented Debate
For coding tasks:
1. Code is extracted from each solution
2. Executed in isolated Docker container
3. Error traces fed back into critique round
4. Only working solutions advance

### Rate Limit Handling
- Sequential API calls to respect limits
- Exponential backoff on failures
- Automatic fallback between providers
- Configurable delays between requests

### Early Stopping
If 3 models agree >90% (via TF-IDF similarity), skip to synthesis to save time and API calls.

## 🛡️ Safety

Code execution uses Docker with:
- Non-root user
- Read-only filesystem
- Network isolation
- Memory limits (512MB)
- CPU limits (0.5 cores)
- Timeout (30s)

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/config` | GET | Current configuration |
| `/api/debate` | POST | Run debate (sync) |
| `/api/execute` | POST | Test code execution |
| `/api/examples` | GET | Example queries |
| `/api/ws/debate` | WS | Real-time streaming |

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Test debate via curl
curl -X POST "http://localhost:8000/api/debate" \
  -H "Content-Type: application/json" \
  -d '{"query": "Calculate the 10th Fibonacci number"}'

# Test code execution
curl -X POST "http://localhost:8000/api/execute" \
  -H "Content-Type: application/json" \
  -d '{"code": "print(sum(range(10)))"}'
```

## 💰 Cost Analysis

| Approach | Monthly Cost | Latency | Quality |
|----------|-------------|---------|---------|
| Claude 3.5 Opus | $20 | Fast | 95% |
| GPT-4o | $20 | Fast | 94% |
| **Council of Frontiers** | **~$0-5** | **15-25s** | **Target: 95%+** |

Cost breakdown (free tiers):
- Groq: 20 req/min free
- Cerebras: 10 req/min free
- Docker: Local (free)
- Redis: Optional (free tier available)

## 🎯 Goals & Metrics

- **GSM8K Math**: Target 95%+ (Opus: 95%)
- **HumanEval Code**: Target 90%+ (Opus: 90%)
- **Hallucination Reduction**: 40% via disagreement detection
- **Total Cost**: <$5 for entire FYP
- **Latency**: 15-25s acceptable for quality gain

## 📝 Citation

Based on:
- Du et al. "Improving Factuality and Reasoning in Language Models through Multiagent Debate" (ICML 2024)
- Together AI "Mixture-of-Agents (MoA)" approach
- FrugalGPT cascading methodology

## 🤝 Contributing

This is a Final Year Project. For FYP demo purposes, the system includes:
- Pre-computed examples for common questions
- Graceful degradation under load
- Real-time visualization for professor demonstrations

## 📜 License

MIT License - Academic Use

---

Built with ❤️ for Final Year Project CSE 2024


