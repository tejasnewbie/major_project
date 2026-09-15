"""Enhanced problem classifier with category detection."""
import re
from typing import Dict, List, Tuple


class ProblemClassifier:
    """Classify problems into categories for strategy selection."""
    
    # Category keywords with weights
    CATEGORIES = {
        "design": {
            "keywords": [
                "design", "ui", "ux", "canvas", "css", "html", "frontend", "layout",
                "color", "style", "visual", "interface", "button", "form", "page",
                "component", "react", "vue", "angular", "svg", "animation", "theme",
                "responsive", "grid", "flexbox", "card", "navbar", "footer", "header"
            ],
            "weight": 2
        },
        "math": {
            "keywords": [
                "calculate", "compute", "solve", "equation", "integral", "derivative",
                "probability", "statistics", "algebra", "geometry", "theorem", "proof",
                "fibonacci", "prime", "factorial", "logarithm", "trigonometry", "matrix",
                "vector", "calculus", "differential", "formula", "solve for", "find the value"
            ],
            "weight": 2
        },
        "code": {
            "keywords": [
                "code", "function", "algorithm", "program", "implement", "debug",
                "python", "javascript", "java", "c++", "rust", "go", "write a",
                "sort", "search", "class", "api", "leetcode", "hackerrank",
                "optimize", "complexity", "o(n)", "recursion", "loop", "array", "list",
                "dictionary", "hashmap", "tree", "graph", "database", "sql"
            ],
            "weight": 2
        },
        "factual": {
            "keywords": [
                "explain", "compare", "analyze", "research", "why", "what is",
                "how does", "difference between", "pros and cons", "advantages",
                "disadvantages", "history of", "overview", "summary", "review",
                "study", "report", "investigation", "evaluation", "assessment"
            ],
            "weight": 1
        },
        "writing": {
            "keywords": [
                "write", "essay", "summarize", "draft", "document", "email",
                "letter", "article", "blog", "post", "content", "description",
                "story", "narrative", "script", "transcript", "message", "proposal",
                "presentation", "speech", "paragraph", "introduction", "conclusion"
            ],
            "weight": 1
        }
    }
    
    @classmethod
    def classify(cls, query: str) -> Tuple[str, float]:
        """
        Classify query into category with confidence score.
        
        Returns:
            Tuple of (category, confidence_score)
        """
        query_lower = query.lower()
        scores = {}
        
        for category, config in cls.CATEGORIES.items():
            score = 0
            for keyword in config["keywords"]:
                if keyword in query_lower:
                    score += config["weight"]
                    # Bonus for exact matches at word boundaries
                    if re.search(r'\b' + re.escape(keyword) + r'\b', query_lower):
                        score += 1
            
            # Normalize by number of keywords
            scores[category] = score / max(len(config["keywords"]) * 0.1, 1)
        
        # Get best category
        if not scores or max(scores.values()) == 0:
            return "general", 0.0
        
        best_category = max(scores, key=scores.get)
        confidence = scores[best_category]
        
        return best_category, confidence
    
    @classmethod
    def get_category_description(cls, category: str) -> str:
        """Get human-readable description of category."""
        descriptions = {
            "design": "UI/UX Design & Frontend",
            "math": "Mathematics & Logic",
            "code": "Programming & Algorithms",
            "factual": "Research & Analysis",
            "writing": "Writing & Documentation",
            "general": "General Question"
        }
        return descriptions.get(category, "General")

    @classmethod
    def assess_difficulty(cls, query: str, category: str = "general") -> str:
        """
        Assess problem difficulty into:
        - 'simple': Greetings, trivial Q&A, short greetings. Directly answered in 1-2s.
        - 'medium': Standard tasks (algorithms like palindrome, short explanations). Answered via fast 2-agent consensus.
        - 'complex': Deep architecture, system design, hard math proofs, lengthy prompts. Full multi-agent debate.
        """
        q = query.strip().lower()
        words = q.split()
        word_count = len(words)

        # 1. Greetings & conversational one-liners
        greeting_patterns = [
            r'^(hi|hello|hey|heya|howdy|yo|sup|greetings|hola)\b',
            r'^good\s+(morning|afternoon|evening|day|night)\b',
            r'^(how are you|who are you|what can you do|what is your name)\b',
            r'^(thanks|thank you|bye|goodbye|see ya)\b'
        ]
        if any(re.search(pat, q) for pat in greeting_patterns):
            return "simple"

        # 2. Trivial short factual / math questions (e.g. "what is 2+2", "capital of france")
        trivial_math = r'^(\d+\s*[\+\-\*\/\^]\s*\d+\s*\??|what is \d+\s*[\+\-\*\/\^]\s*\d+\s*\??)$'
        if re.match(trivial_math, q):
            return "simple"

        if word_count <= 6 and not any(k in q for k in ["design", "architecture", "complex", "implement", "optimize", "system"]):
            if category in ["general", "factual"]:
                return "simple"

        # 3. Complex prompts
        complex_indicators = [
            "architecture", "system design", "distributed", "microservices",
            "end-to-end", "step by step proof", "formal proof", "in-depth analysis",
            "full stack", "production ready", "multi-tier", "comprehensive review"
        ]
        if word_count > 60 or any(ci in q for ci in complex_indicators):
            return "complex"

        if category == "design" and word_count > 25:
            return "complex"

        # Default standard queries (palindrome, explain X, moderate coding/math)
        return "medium"


# Backward compatibility
ProblemTypeClassifier = ProblemClassifier

