"""Query Classifier - Categorizes user queries into predefined types.

This module determines if a query is company-related, general knowledge,
ambiguous, or restricted (handled by compliance filter).
"""

from typing import Literal, List
from dataclasses import dataclass
import re

from config.settings import Settings

QueryType = Literal["company", "general", "ambiguous"]

@dataclass
class QueryClassifier:
    """Classifies user queries into types for appropriate handling.

    Attributes:
        settings: Application settings object
        company_keywords: List of keywords indicating company-related queries
    """
    settings: Settings
    company_keywords: List[str] = None

    def __post_init__(self) -> None:
        """Initialize company keywords list."""
        if self.company_keywords is None:
            self.company_keywords = [
                # Company policies
                "zuru melon", "company policy", "code of conduct", "ai ethics",
                "data security", "confidentiality", "intellectual property",
                "remote work", "diversity", "inclusion",
                
                # Procedures
                "hiring", "onboarding", "vacation", "leave request",
                "ai project", "client onboarding", "complaints",
                
                # Coding style
                "coding style", "pep 8", "typescript", "python",
                "naming convention", "testing", "linting", "ci/cd",
                
                # HR
                "hr", "sick leave", "working hours", "30-60-90 day plan"
            ]

    def classify(self, query: str) -> QueryType:
        """Classify a user query into one of the predefined types.

        Args:
            query: User input string to classify

        Returns:
            Query type (company, general, ambiguous)
        """
        if not query or not isinstance(query, str):
            return "ambiguous"

        query_lower = query.lower()

        # Count company keyword matches
        company_matches = sum(
            1 for keyword in self.company_keywords 
            if re.search(rf"\b{re.escape(keyword)}\b", query_lower)
        )

        # Classify based on matches
        if company_matches >= 1:
            return "company"
        elif self._is_general_knowledge(query_lower):
            return "general"
        else:
            return "ambiguous"

    def _is_general_knowledge(self, query: str) -> bool:
        """Check if a query is general knowledge.

        Args:
            query: Lowercase user query string

        Returns:
            True if general knowledge, False otherwise
        """
        # General knowledge indicators
        general_patterns = [
            r"what is|who is|how to",
            r"\bpython\b(?! coding| style| convention)",
            r"\bai\b(?! ethics| policy| project)",
            r"general knowledge|definition|explain",
            r"weather|news|sports|history",
            r"math|science|technology (?! zuru| melon)"
        ]

        return any(re.search(pattern, query) for pattern in general_patterns)