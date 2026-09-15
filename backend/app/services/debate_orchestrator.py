"""
Council of Frontiers - Debate Orchestrator
Implements: Iterative Refinement + Hierarchical Synthesis
"""
import asyncio
import json
import re
from typing import List, Dict, Any, Optional, AsyncGenerator
from dataclasses import dataclass, field
from datetime import datetime
import logging

from app.core.config import get_settings, REASONING_PROMPTS, CRITIQUE_SYSTEM_PROMPT
from app.core.classifier import ProblemClassifier
from app.core.strategies import get_strategy, SolutionScore
from app.services.llm_client import LLMClientManager, LLMResponse
from app.services.code_executor import CodeExecutor, get_executor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class AgentResponse:
    """Response from a single agent."""
    round_num: int
    agent_id: str
    provider: str
    model: str
    content: str
    reasoning_style: Optional[str] = None
    latency: float = 0.0
    tokens_used: Optional[int] = None
    execution_result: Optional[Dict] = None


@dataclass
class DebateResult:
    """Complete debate result."""
    query: str
    problem_type: str
    category: str
    round1_responses: List[AgentResponse] = field(default_factory=list)
    refinement_responses: List[AgentResponse] = field(default_factory=list)
    scores: List[SolutionScore] = field(default_factory=list)
    winner_idx: int = 0
    final_answer: str = ""
    confidence_score: float = 0.0
    total_latency: float = 0.0
    early_stopped: bool = False
    execution_feedback: List[Dict] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class DebateOrchestrator:
    """
    4-Round Debate with Iterative Refinement:
    1. Generation (3 models create solutions)
    2. Evaluation (Score all solutions)
    3. Refinement (2 models improve the winner)
    4. Synthesis (Hierarchical: select + polish)
    """
    
    def __init__(self):
        self.settings = get_settings()
        self.llm_manager = LLMClientManager(self.settings)
        self.executor = get_executor()
    
    async def run_debate(
        self, 
        query: str,
        stream: bool = True
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Run the 4-round debate process."""
        start_time = datetime.now()
        result = DebateResult(query=query, problem_type="", category="")
        
        # === ROUND 0: Classification ===
        category, confidence = ProblemClassifier.classify(query)
        result.category = category
        result.problem_type = category
        
        strategy = get_strategy(category, self.settings)
        model_config = strategy.get_round_config()
        
        yield self._create_progress("classification", 
            f"Category: {ProblemClassifier.get_category_description(category)}",
            {"category": category, "confidence": confidence})
        
        # === ROUND 1: Generation ===
        yield self._create_progress("round1_start", "Generation: Creating solutions...")
        
        gen_config = model_config["generation"]
        gen_tasks = [
            self._generate_solution(query, category, f"agent_{i+1}", config)
            for i, config in enumerate(gen_config)
        ]
        
        round1_responses = []
        for completed_task in asyncio.as_completed(gen_tasks):
            response = await completed_task
            round1_responses.append(response)
            yield self._create_progress("round1_progress",
                f"[OK] {response.provider}/{response.model.split('/')[-1][:20]}",
                {"agent": response.agent_id, "latency": f"{response.latency:.1f}s"})
        
        # Sort responses by agent_id to keep consistent order (agent_1, agent_2, agent_3)
        round1_responses.sort(key=lambda r: r.agent_id)
        result.round1_responses = round1_responses
        
        # === ROUND 2: Evaluation (Scoring) ===
        yield self._create_progress("evaluation", "Evaluating solutions...")
        
        # Code execution if applicable
        if category == "code":
            yield self._create_progress("execution", "Testing code...")
            execution_results = await self._test_code_solutions(round1_responses)
            result.execution_feedback = execution_results
            for i, response in enumerate(round1_responses):
                if i < len(execution_results):
                    response.execution_result = execution_results[i]
        
        # Score all solutions
        scores = await strategy.evaluate_solutions(query, round1_responses, self.llm_manager)
        result.scores = scores
        
        # Log scores
        for score in sorted(scores, key=lambda x: x.total_score, reverse=True):
            logger.info(f"Solution {score.solution_idx}: {score.total_score}/20 - {score.summary}")
        
        # Check early stop
        if strategy.should_skip_critique(round1_responses, scores):
            yield self._create_progress("early_stop", "High quality detected, optimizing...")
        
        # Pick winner
        winner_idx = max(scores, key=lambda x: x.total_score).solution_idx
        result.winner_idx = winner_idx
        winner = round1_responses[winner_idx]
        
        yield self._create_progress("winner_selected", 
            f"Best solution: Agent {winner_idx + 1} (Score: {scores[winner_idx].total_score}/20)",
            {"winner": winner_idx, "score": scores[winner_idx].total_score})
        
        # === ROUND 3: Refinement (Iterative Improvement) ===
        yield self._create_progress("refinement_start", "Refinement: Improving winner...")
        
        # Generate critiques first (needed for refinement)
        critiques = await self._generate_critiques(query, winner, round1_responses, strategy)
        
        # Now refine with 2 models
        refinement_config = model_config.get("refinement", [model_config["synthesis"]])
        refinement_tasks = [
            strategy.refine_solution(query, winner, critiques, self.llm_manager, config)
            for config in refinement_config[:2]  # Max 2 refiners
        ]
        
        refinement_responses = []
        for completed_task in asyncio.as_completed(refinement_tasks):
            response = await completed_task
            refinement_responses.append(response)
            yield self._create_progress("refinement_progress",
                f"[OK] Improved by {response.provider}",
                {"refiner": response.agent_id, "latency": f"{response.latency:.1f}s"})
        
        refinement_responses.sort(key=lambda r: r.agent_id)
        result.refinement_responses = refinement_responses
        
        # === ROUND 4: Synthesis (Hierarchical) ===
        yield self._create_progress("synthesis_start", "Synthesis: Finalizing...")
        
        final_response = await strategy.hierarchical_synthesis(
            query=query,
            winner=winner,
            improved_versions=refinement_responses,
            llm_manager=self.llm_manager
        )
        
        result.final_answer = final_response.content
        result.confidence_score = scores[winner_idx].total_score / 20.0
        result.total_latency = (datetime.now() - start_time).total_seconds()
        
        yield self._create_progress("complete", 
            f"Complete! (Total: {result.total_latency:.1f}s)",
            {"latency": result.total_latency, "confidence": result.confidence_score})
        
        yield self._create_final_result(result)
    
    async def _generate_solution(
        self,
        query: str,
        category: str,
        agent_id: str,
        config: Dict
    ) -> AgentResponse:
        """Generate initial solution."""
        provider = config["provider"]
        model = config["model"]
        reasoning_style = config.get("reasoning_style", "structured")
        
        style_prompts = REASONING_PROMPTS.get(category, REASONING_PROMPTS["general"])
        reasoning_instruction = style_prompts.get(reasoning_style) or style_prompts.get("structured") or list(style_prompts.values())[0]
        
        system_prompt = f"""You are an expert. {reasoning_instruction}

Provide a complete, high-quality solution."""

        response = await self.llm_manager.generate_with_fallback(
            primary_provider=provider,
            model=model,
            prompt=f"Task: {query}",
            system_prompt=system_prompt,
            temperature=0.7,
            max_tokens=1500
        )
        
        return AgentResponse(
            round_num=1,
            agent_id=agent_id,
            provider=response.provider,
            model=response.model,
            content=response.content,
            reasoning_style=reasoning_style,
            latency=response.latency,
            tokens_used=response.tokens_used
        )
    
    async def _generate_critiques(
        self,
        query: str,
        winner: AgentResponse,
        all_solutions: List[AgentResponse],
        strategy
    ) -> List[AgentResponse]:
        """Generate critiques for refinement."""
        critiques = []
        
        # Get 2 strongest models to critique
        model_config = strategy.get_round_config()
        # Use fast groq models for critiquing
        critique_configs = [
            model_config.get("scoring", {"provider": "groq", "model": "llama-3.3-70b-versatile"}),
            {"provider": "groq", "model": "llama-3.1-8b-instant"}
        ]
        
        for i, config in enumerate(critique_configs[:2]):
            provider = config["provider"]
            model = config["model"]
            
            # Summarize for token limit
            solutions_summary = strategy.summarize_for_model(all_solutions, provider)
            
            prompt = f"""Critique these solutions for: {query}

SOLUTIONS:
{solutions_summary}

Identify bugs, missing features, and improvements needed. Be specific."""
            
            response = await self.llm_manager.generate_with_fallback(
                primary_provider=provider,
                model=model,
                prompt=prompt,
                system_prompt=CRITIQUE_SYSTEM_PROMPT,
                temperature=0.5,
                max_tokens=3000
            )
            
            critiques.append(AgentResponse(
                round_num=2,
                agent_id=f"critic_{i+1}",
                provider=response.provider,
                model=response.model,
                content=response.content,
                latency=response.latency
            ))
        
        return critiques
    
    async def _test_code_solutions(
        self, 
        responses: List[AgentResponse]
    ) -> List[Dict]:
        """Execute and test code solutions."""
        results = []
        
        for response in responses:
            code = self._extract_code(response.content)
            if not code:
                results.append({
                    "agent_id": response.agent_id,
                    "status": "no_code",
                    "error": "No code found"
                })
                continue
            
            is_valid, error = await self.executor.validate_syntax(code)
            if not is_valid:
                results.append({
                    "agent_id": response.agent_id,
                    "status": "syntax_error",
                    "error": error
                })
                continue
            
            exec_result = await self.executor.execute(code)
            results.append({
                "agent_id": response.agent_id,
                "status": "executed",
                "exit_code": exec_result.exit_code,
                "stdout": exec_result.stdout[:500],
                "stderr": exec_result.stderr[:300],
                "works": exec_result.exit_code == 0 and not exec_result.stderr
            })
        
        return results
    
    def _extract_code(self, content: str) -> Optional[str]:
        """Extract code blocks."""
        patterns = [
            r'```python\n(.*?)```',
            r'```\n(.*?)```',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.DOTALL)
            if matches:
                return matches[0].strip()
        
        if 'def ' in content or 'class ' in content:
            return content
        
        return None
    
    def _create_progress(self, stage: str, message: str, data: Dict = None) -> Dict:
        return {
            "type": "progress",
            "stage": stage,
            "message": message,
            "data": data or {},
            "timestamp": datetime.now().isoformat()
        }
    
    def _create_final_result(self, result: DebateResult) -> Dict:
        return {
            "type": "complete",
            "result": {
                "query": result.query,
                "category": result.category,
                "final_answer": result.final_answer,
                "confidence": result.confidence_score,
                "latency": result.total_latency,
                "winner": result.winner_idx,
                "scores": [
                    {"idx": s.solution_idx, "score": s.total_score, "summary": s.summary}
                    for s in result.scores
                ],
                "round1": [
                    {"agent": r.agent_id, "provider": r.provider, 
                     "model": r.model.split('/')[-1][:30], "latency": r.latency,
                     "content": r.content, "reasoning_style": r.reasoning_style}
                    for r in result.round1_responses
                ],
                "refinements": [
                    {"agent": r.agent_id, "provider": r.provider, "latency": r.latency,
                     "content": r.content}
                    for r in result.refinement_responses
                ]
            }
        }
    
    async def close(self):
        await self.llm_manager.close_all()
