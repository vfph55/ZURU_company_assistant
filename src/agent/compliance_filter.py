"""Compliance Filter Module - Filter restricted or harmful content.

This module checks user queries against company policies to block harmful,
inappropriate, or policy-violating content before processing.
"""

from typing import List, Optional
from dataclasses import dataclass
import re

from config.settings import Settings

@dataclass
class ComplianceFilter:
    """Filter user queries against company policies.

    Attributes:
        settings: System settings object
        restricted_patterns: List of regex patterns for restricted content
        restricted_topics: List of topics that violate company policy
    """
    settings: Settings
    restricted_patterns: Optional[List[str]] = None
    restricted_topics: Optional[List[str]] = None

    def __post_init__(self) -> None:
        """Initialize restricted content patterns/topics after creation."""
        if self.restricted_patterns is None:
            self.restricted_patterns = [
                r"hack|crack|phish",
                r"discriminat(e|ion)|harass",
                r"leak|share confidential data",
                r"unethical ai|bias in ai (ignore|disable)",
                r"bypass security|data breach",
                r"copyright infringement|piracy",
            ]
        
        if self.restricted_topics is None:
            self.restricted_topics = [
                "share client data",
                "use company IP for personal projects",
                "disable AI ethics audits",
                "lie to clients about capabilities",
                "skip cybersecurity training",
                "discriminate in hiring",
            ]

    def is_allowed(self, query: str) -> bool:
        """Check if a query complies with ZURU's guidelines.

        Args:
            query: User input string to check

        Returns:
            True if query is allowed, False otherwise
        """
        if not query or not isinstance(query, str):
            return False

        query_lower = query.lower()

        # Check regex patterns
        for pattern in self.restricted_patterns:
            if re.search(pattern, query_lower):
                return False

        # Check restricted topics
        for topic in self.restricted_topics:
            if topic in query_lower:
                return False

        return True