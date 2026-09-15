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


# Backward compatibility
ProblemTypeClassifier = ProblemClassifier
