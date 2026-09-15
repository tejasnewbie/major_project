"""Category-based debate strategies with Iterative Refinement + Hierarchical Synthesis."""
import json
import re
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import logging

from app.core.config import (
    get_settings, REASONING_PROMPTS, REFINEMENT_PROMPTS, 
    SYNTHESIS_STEP_PROMPTS, CRITIQUE_SYSTEM_PROMPT,
    CATEGORY_MODEL_CONFIG
)

logger = logging.getLogger(__name__)


@dataclass
class SolutionScore:
    """Score for a solution."""
    solution_idx: int
    total_score: float
    breakdown: Dict[str, float]
    summary: str


class BaseStrategy(ABC):
    """Base class for debate strategies with iterative refinement."""
    
    TOKEN_LIMITS = {
        "groq": 8000,
        "open_router": 16000,
        "nvidia": 16000,  # Kimi K2.5 has larger context
    }
    
    MAX_OUTPUT_TOKENS = 4000
    
    def __init__(self, settings, category: str):
        self.settings = settings
        self.category = category
        self.model_config = CATEGORY_MODEL_CONFIG.get(category, CATEGORY_MODEL_CONFIG["general"])
    
    def get_round_config(self) -> Dict[str, Any]:
        """Get model configuration for this strategy."""
        return self.model_config
    
    @abstractmethod
    async def evaluate_solutions(
        self, 
        query: str,
        solutions: List[Any],
        llm_manager
    ) -> List[SolutionScore]:
        """Evaluate and score solutions."""
        pass
    
    async def refine_solution(
        self,
        query: str,
        winner: Any,
        critiques: List[Any],
        llm_manager,
        refinement_config: Dict
    ) -> Any:
        """
        Iterative Refinement: Improve the winning solution.
        Instead of critiquing, models actually improve the winner.
        """
        provider = refinement_config["provider"]
        model = refinement_config["model"]
        
        winner_content = getattr(winner, 'content', str(winner))
        winner_provider = getattr(winner, 'provider', 'unknown')
        
        # Prepare critiques summary
        critiques_text = []
        for i, crit in enumerate(critiques, 1):
            content = getattr(crit, 'content', str(crit))
            # Truncate critiques
            truncated = self.truncate_text(content, 2000)
            critiques_text.append(f"Feedback {i}:\n{truncated}")
        
        critiques_joined = '\n\n---\n\n'.join(critiques_text)
        
        # Get category-specific refinement prompt
        refinement_instruction = REFINEMENT_PROMPTS.get(
            self.category, 
            REFINEMENT_PROMPTS["general"]
        )
        
        system_prompt = f"""{REFINEMENT_PROMPTS['system']}

{refinement_instruction}"""

        user_prompt = f"""Original Request: {query}

CURRENT BEST SOLUTION (from {winner_provider}):
{self.truncate_text(winner_content, 4000)}

FEEDBACK TO ADDRESS:
{critiques_joined}

Provide the COMPLETE IMPROVED SOLUTION."""

        response = await llm_manager.generate_with_fallback(
            primary_provider=provider,
            model=model,
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.4,  # Lower for focused improvements
            max_tokens=self.MAX_OUTPUT_TOKENS
        )
        
        # Create improved response object
        from app.services.debate_orchestrator import AgentResponse
        return AgentResponse(
            round_num=3,  # Refinement round
            agent_id=f"refiner_{provider}",
            provider=response.provider,
            model=response.model,
            content=response.content,
            latency=response.latency,
            tokens_used=response.tokens_used
        )
    
    async def hierarchical_synthesis(
        self,
        query: str,
        winner: Any,
        improved_versions: List[Any],
        llm_manager
    ) -> Any:
        """
        Hierarchical Synthesis: Step-by-step polishing.
        Step 1: Select best from improved versions
        Step 2: Apply final polish
        """
        synth_config = self.model_config["synthesis"]
        provider = synth_config["provider"]
        model = synth_config["model"]
        
        # Step 1: Select best from all versions (original + improvements)
        all_versions = [winner] + improved_versions
        
        options_text = []
        for i, v in enumerate(all_versions, 1):
            v_content = getattr(v, "content", str(v))
            v_provider = getattr(v, "provider", "unknown")
            options_text.append(f"Option {i} (from {v_provider}):\n{self.truncate_text(v_content, 2000)}")
        options_joined = "\n\n---\n\n".join(options_text)
        
        select_prompt = f"""Select the single best solution for: {query}

OPTIONS:
{options_joined}

{SYNTHESIS_STEP_PROMPTS['select']}

Reply ONLY with the number of the best option (e.g. 1, 2, or 3)."""

        select_response = await llm_manager.generate_with_fallback(
            primary_provider=provider,
            model=model,
            prompt=select_prompt,
            temperature=0.3,
            max_tokens=200
        )
        
        # Extract selected index
        try:
            # Find number in response
            import re
            numbers = re.findall(r'\d+', select_response.content)
            selected_idx = int(numbers[0]) - 1 if numbers else 0
            selected_idx = max(0, min(selected_idx, len(all_versions) - 1))
        except:
            selected_idx = 0
        
        best_solution = all_versions[selected_idx]
        best_content = getattr(best_solution, 'content', str(best_solution))
        
        # Step 2: Final polish
        polish_prompt = f"""Final polish for: {query}

{SYNTHESIS_STEP_PROMPTS['polish']}

SOLUTION TO POLISH:
{self.truncate_text(best_content, 6000)}

Provide the FINAL, PRODUCTION-READY solution."""

        final_response = await llm_manager.generate_with_fallback(
            primary_provider=provider,
            model=model,
            prompt=polish_prompt,
            temperature=0.3,
            max_tokens=self.MAX_OUTPUT_TOKENS
        )
        
        return final_response
    
    def truncate_text(self, text: str, max_tokens: int = 3000) -> str:
        """Truncate text to fit within token limit."""
        if not text:
            return text
        
        char_limit = max_tokens * 3
        
        if len(text) <= char_limit:
            return text
        
        truncated = text[:char_limit]
        last_period = truncated.rfind('.')
        last_space = truncated.rfind(' ')
        
        if last_period > char_limit * 0.8:
            truncated = truncated[:last_period + 1]
        elif last_space > 0:
            truncated = truncated[:last_space]
        
        return truncated + f"\n\n[... Content truncated ({len(text)} chars total) ...]"
    
    def summarize_for_model(self, items: List[Any], provider: str) -> str:
        """Summarize items for a specific model's token limit."""
        max_tokens = self.TOKEN_LIMITS.get(provider, 8000)
        available = max_tokens - 2000
        
        summaries = []
        for i, item in enumerate(items, 1):
            content = getattr(item, 'content', str(item))
            summary = f"Option {i}:\n{self.truncate_text(content, available // len(items))}"
            summaries.append(summary)
        
        return '\n\n---\n\n'.join(summaries)
    
    def should_skip_critique(self, solutions: List[Any], scores: List[SolutionScore]) -> bool:
        """Override in subclasses."""
        return False


class DesignStrategy(BaseStrategy):
    """Strategy for design/creative tasks with visual scoring."""
    
    async def evaluate_solutions(
        self,
        query: str,
        solutions: List[Any],
        llm_manager
    ) -> List[SolutionScore]:
        """Score design solutions on multiple dimensions."""
        scores = []
        
        scoring_config = self.model_config["scoring"]
        
        for i, sol in enumerate(solutions):
            content = getattr(sol, 'content', str(sol))
            truncated = self.truncate_text(content, 2000)
            
            prompt = f"""Score this design solution (0-10 each):

CRITERIA:
1. CREATIVITY: Is it innovative and visually appealing?
2. FUNCTIONALITY: Does it meet all requirements?
3. CODE_QUALITY: Clean, maintainable implementation?
4. COMPLETENESS: All features implemented?

Request: {query}

Solution:
{truncated}

Output JSON:
{{"creativity": 8, "functionality": 9, "code_quality": 7, "completeness": 8, "total": 32, "summary": "Brief assessment"}}"""

            try:
                response = await llm_manager.generate_with_fallback(
                    primary_provider=scoring_config["provider"],
                    model=scoring_config["model"],
                    prompt=prompt,
                    temperature=0.3,
                    max_tokens=300
                )
                
                result = self._extract_json(response.content)
                if result:
                    scores.append(SolutionScore(
                        solution_idx=i,
                        total_score=result.get("total", 20),
                        breakdown={
                            "creativity": result.get("creativity", 5),
                            "functionality": result.get("functionality", 5),
                            "code_quality": result.get("code_quality", 5),
                            "completeness": result.get("completeness", 5),
                        },
                        summary=result.get("summary", "No summary")
                    ))
                else:
                    scores.append(self._default_score(i))
            except Exception as e:
                logger.error(f"Scoring error: {e}")
                scores.append(self._default_score(i))
        
        return scores
    
    def _extract_json(self, text: str) -> Optional[Dict]:
        try:
            json_match = re.search(r'\{[^}]+\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return json.loads(text)
        except:
            return None
    
    def _default_score(self, idx: int) -> SolutionScore:
        return SolutionScore(
            solution_idx=idx,
            total_score=20,
            breakdown={"creativity": 5, "functionality": 5, "code_quality": 5, "completeness": 5},
            summary="Default score"
        )
    
    def should_skip_critique(self, solutions: List[Any], scores: List[SolutionScore]) -> bool:
        """Skip refinement if one solution is clearly superior."""
        if len(scores) >= 2:
            sorted_scores = sorted(scores, key=lambda x: x.total_score, reverse=True)
            if sorted_scores[0].total_score - sorted_scores[1].total_score >= 5:
                return True
        return False


class MathStrategy(BaseStrategy):
    """Strategy for math/logic tasks with correctness checking."""
    
    async def evaluate_solutions(
        self,
        query: str,
        solutions: List[Any],
        llm_manager
    ) -> List[SolutionScore]:
        """Score based on correctness and rigor."""
        scores = []
        
        # Extract answers
        answers = []
        for sol in solutions:
            content = getattr(sol, 'content', str(sol))
            answer = self._extract_final_answer(content)
            answers.append(answer)
        
        # Check consensus
        from collections import Counter
        answer_counts = Counter(answers)
        majority_answer, majority_count = answer_counts.most_common(1)[0] if answer_counts else ("", 0)
        
        for i, sol in enumerate(solutions):
            content = getattr(sol, 'content', str(sol))
            answer = answers[i]
            
            is_correct = answer == majority_answer and majority_count >= 2
            has_steps = any(marker in content.lower() for marker in ['step', '1.', '→', 'therefore'])
            has_proof = any(marker in content.lower() for marker in ['proof', 'q.e.d', '∎'])
            shows_work = '=' in content or '→' in content
            
            score = SolutionScore(
                solution_idx=i,
                total_score=(12 if is_correct else 3) + (3 if has_steps else 0) + 
                           (2 if has_proof else 0) + (3 if shows_work else 0),
                breakdown={
                    "correctness": 12 if is_correct else 3,
                    "showing_work": 3 if has_steps else 0,
                    "rigor": 2 if has_proof else 0,
                    "clarity": 3 if shows_work else 0,
                },
                summary=f"Answer: {answer[:30]}, Correct: {is_correct}"
            )
            scores.append(score)
        
        return scores
    
    def _extract_final_answer(self, content: str) -> str:
        patterns = [
            r'(?:answer|result|equals?|is)\s*:?\s*([\d\w\s\-\.]+?)(?:\.|$|\n)',
            r'(?:therefore|thus|so)\s*,?\s*([\d\w\s\-\.]+?)(?:\.|$|\n)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content.lower())
            if match:
                return match.group(1).strip()[:50]
        
        lines = [l.strip() for l in content.split(chr(10)) if l.strip()]
        return lines[-1][:50] if lines else ""
    
    def should_skip_critique(self, solutions: List[Any], scores: List[SolutionScore]) -> bool:
        """Skip if 2+ models agree with high confidence."""
        correct_solutions = [s for s in scores if s.breakdown.get("correctness", 0) >= 10]
        if len(correct_solutions) >= 2:
            return True
        return False


class CodeStrategy(BaseStrategy):
    """Strategy for coding tasks with execution testing."""
    
    async def evaluate_solutions(
        self,
        query: str,
        solutions: List[Any],
        llm_manager
    ) -> List[SolutionScore]:
        """Score based on execution and code quality."""
        scores = []
        
        for i, sol in enumerate(solutions):
            content = getattr(sol, 'content', str(sol))
            execution = getattr(sol, 'execution_result', None)
            
            if execution:
                exit_code = execution.get('exit_code', -1)
                has_errors = execution.get('stderr', '') != ''
                works = exit_code == 0 and not has_errors
                
                # Execution is 60% of score
                execution_score = 12 if works else 2
            else:
                execution_score = 6  # Neutral if not tested
            
            # Code quality heuristics
            has_functions = 'def ' in content
            has_error_handling = 'try:' in content or 'if __name__' in content
            has_comments = '#' in content or '"""' in content
            has_types = '->' in content or ': ' in content.split(chr(10))[0] if content else False
            
            score = SolutionScore(
                solution_idx=i,
                total_score=execution_score + 
                           (2 if has_functions else 0) + 
                           (2 if has_error_handling else 0) + 
                           (1 if has_comments else 0) + 
                           (1 if has_types else 0),
                breakdown={
                    "execution": execution_score,
                    "structure": 2 if has_functions else 0,
                    "robustness": 2 if has_error_handling else 0,
                    "documentation": 1 if has_comments else 0,
                },
                summary="Works" if execution_score >= 10 else "Has issues"
            )
            scores.append(score)
        
        return scores


class FactualStrategy(BaseStrategy):
    """Strategy for factual/research questions."""
    
    async def evaluate_solutions(
        self,
        query: str,
        solutions: List[Any],
        llm_manager
    ) -> List[SolutionScore]:
        """Score on completeness and accuracy."""
        scores = []
        
        for i, sol in enumerate(solutions):
            content = getattr(sol, 'content', str(sol))
            
            has_structure = any(m in content for m in [chr(10)+chr(10), '1.', '- '])
            has_examples = 'example' in content.lower() or 'e.g.' in content.lower()
            has_sources = any(m in content for m in ['according to', 'study', 'research'])
            length_score = min(len(content) / 500, 4)
            
            score = SolutionScore(
                solution_idx=i,
                total_score=(3 if has_structure else 0) + 
                           (3 if has_examples else 0) + 
                           (2 if has_sources else 0) + 
                           length_score + 8,  # Base score
                breakdown={
                    "structure": 3 if has_structure else 0,
                    "examples": 3 if has_examples else 0,
                    "sources": 2 if has_sources else 0,
                    "thoroughness": length_score,
                },
                summary="Well-researched" if has_sources else "Good overview"
            )
            scores.append(score)
        
        return scores
    
    def should_skip_critique(self, solutions: List[Any], scores: List[SolutionScore]) -> bool:
        """Always do light refinement for factual."""
        return False


class WritingStrategy(BaseStrategy):
    """Strategy for writing/text generation."""
    
    async def evaluate_solutions(
        self,
        query: str,
        solutions: List[Any],
        llm_manager
    ) -> List[SolutionScore]:
        """Score on style and clarity."""
        scores = []
        
        for i, sol in enumerate(solutions):
            content = getattr(sol, 'content', str(sol))
            
            sentences = len([s for s in content.split('.') if s.strip()])
            has_structure = (chr(10) + chr(10)) in content
            appropriate_length = 3 if 100 < len(content) < 2000 else 1
            has_voice = any(m in content for m in ['!', '?', '--']) or sentences > 3
            
            score = SolutionScore(
                solution_idx=i,
                total_score=min(sentences / 3, 5) + 
                           (3 if has_structure else 0) + 
                           appropriate_length + 
                           (2 if has_voice else 0) + 8,
                breakdown={
                    "flow": min(sentences / 3, 5),
                    "structure": 3 if has_structure else 0,
                    "length": appropriate_length,
                    "voice": 2 if has_voice else 0,
                },
                summary="Well-written" if has_structure else "Needs polish"
            )
            scores.append(score)
        
        return scores
    
    def should_skip_critique(self, solutions: List[Any], scores: List[SolutionScore]) -> bool:
        """Skip if one style is clearly best."""
        sorted_scores = sorted(scores, key=lambda x: x.total_score, reverse=True)
        if len(sorted_scores) >= 2:
            if sorted_scores[0].total_score - sorted_scores[1].total_score >= 4:
                return True
        return False


class GeneralStrategy(BaseStrategy):
    """Fallback strategy."""
    
    async def evaluate_solutions(
        self,
        query: str,
        solutions: List[Any],
        llm_manager
    ) -> List[SolutionScore]:
        """General quality evaluation."""
        scores = []
        
        for i, sol in enumerate(solutions):
            content = getattr(sol, 'content', str(sol))
            
            is_complete = len(content) > 100
            has_structure = any(m in content for m in [chr(10)+chr(10), '1.', '- '])
            
            score = SolutionScore(
                solution_idx=i,
                total_score=(6 if is_complete else 2) + (4 if has_structure else 0) + 10,
                breakdown={
                    "completeness": 6 if is_complete else 2,
                    "structure": 4 if has_structure else 0,
                },
                summary="Complete" if is_complete else "Brief"
            )
            scores.append(score)
        
        return scores


def get_strategy(category: str, settings) -> BaseStrategy:
    """Get strategy for category."""
    strategies = {
        "design": DesignStrategy,
        "math": MathStrategy,
        "code": CodeStrategy,
        "factual": FactualStrategy,
        "writing": WritingStrategy,
        "general": GeneralStrategy,
    }
    strategy_class = strategies.get(category, GeneralStrategy)
    return strategy_class(settings, category)
