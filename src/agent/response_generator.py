"""Response Generator - Synthesizes answers from relevant sources.

This module creates final, formatted responses for users by combining
context from the knowledge base or external search with clear attribution.
"""

from typing import Literal
from dataclasses import dataclass

from config.settings import Settings

QueryType = Literal["company", "general", "ambiguous"]

@dataclass
class ResponseGenerator:
    """Generates formatted responses for user queries.

    Attributes:
        settings: System settings object
    """
    settings: Settings

    def generate(self, query: str, context: str, query_type: QueryType) -> str:
        """Generate a final response for the user.

        Args:
            query: Original user query
            context: Relevant context from KB or external search
            query_type: Type of query (company/general/ambiguous)

        Returns:
            Formatted, user-friendly response
        """
        if query_type == "company":
            return self._format_company_response(query, context)
        elif query_type == "general":
            return self._format_general_response(query, context)
        elif query_type == "ambiguous":
            return "Could you clarify your question? It's unclear if this is about ZURU company or general knowledge."
        else:
            return "I'm unable to answer this query at this time. Please try rephrasing or contact HR/Engineering for assistance."

    def _format_company_response(self, query: str, context: str) -> str:
        """Format responses for company-related queries.

        Args:
            query: Original user query
            context: Relevant content from company KB

        Returns:
            Formatted response with source attribution
        """
        if not context:
            return f"No specific information found for: '{query}'. Please check the company intranet or contact policies@zurumelon.com."

        # Add introductory text for company responses
        intro = f"Here's the relevant information from ZURU Melon's official documentation for your query: '{query}'\n\n"
        footer = "\n\nFor more details, refer to the full documents on the company intranet or contact policies@zurumelon.com."

        return f"{intro}{context}{footer}"

    def _format_general_response(self, query: str, context: str) -> str:
        """Format responses for general knowledge queries.

        Args:
            query: Original user query
            context: Response from external search API

        Returns:
            Formatted general knowledge response
        """
        if not context:
            return f"No information found for general knowledge query: '{query}'. Please try rephrasing your question."

        # Add introductory text for general responses
        intro = f"Here's the answer to your question: \n\n"
        footer = "\n\nThis information is from external sources and not official ZURU Melon content."

        return f"{intro}{context}{footer}"