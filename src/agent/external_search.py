"""External Search Module - Handles general knowledge queries via OpenRouter API.

This module uses the OpenRouter API to answer general knowledge questions,
adhering to cost-efficiency and ethical guidelines.
"""

import os
from typing import Dict, Optional
from dataclasses import dataclass
import requests

from config.settings import Settings
from utils.logger import get_logger

logger = get_logger(__name__)

@dataclass
class ExternalSearch:
    """Handles external search/general knowledge queries via OpenRouter API.

    Attributes:
        settings: System settings object
        api_key: OpenRouter API key
        base_url: OpenRouter API base URL
        headers: API request headers
    """
    settings: Settings
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    headers: Optional[Dict[str, str]] = None

    def __post_init__(self) -> None:
        """Initialize API configuration."""
        self.api_key = self.settings.openrouter_api_key
        self.base_url = self.settings.openrouter_base_url

        if not self.api_key:
            raise ValueError("OpenRouter API key not found in settings")

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def search(self, query: str) -> str:
        """Execute a general knowledge query via OpenRouter API.

        Args:
            query: User's general knowledge question

        Returns:
            Formatted response from the API
        """
        prompt = f"""
        Answer this general knowledge question clearly and concisely:
        Question: {query}
        
        Guidelines:
        1. Keep answers under 300 words
        2. Be accurate and factual
        3. Prioritize up-to-date information (2024-2026) if applicable
        4. Avoid speculation
        5. Do not include harmful/unethical content
        6. If the question is about ZURU Melon and no up-to-date info is found, state "No latest updates available for ZURU Melon's {query}"

        """

        # API request payload (using lightweight model for cost efficiency)
        payload = {
            "model": "openai/gpt-5.2", 
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 300,  # Limit response length to control cost
            "temperature": 0.7
        }

        try:
            # Send request to OpenRouter API
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=10
            )
            response.raise_for_status()

            # Parse response
            data = response.json()
            answer = data["choices"][0]["message"]["content"].strip()

            # Log API usage (for cost tracking)
            logger.info(
                f"OpenRouter API Usage - Tokens: {data['usage']['total_tokens']}, "
                f"Query: {query[:50]}..."
            )

            return answer

        except requests.exceptions.RequestException as e:
            logger.error(f"External search failed: {str(e)}")
            return ""
    
    def real_time_search(self, query: str) -> str:
        """Retrieve real-time information using SerpAPI.

        Args:
            query: The original user query string

        Returns:
            A formatted string containing summarized search results from SerpAPI.
            Returns an empty string if the API key is missing or the request fails.
        """
        if not os.getenv("SERP_API_KEY"):
            return ""

        params = {
            "q": query + "site:zurumelon.com",  # Limit search to ZURU's official website
            "api_key": os.getenv("SERP_API_KEY"),
            "num": 3
        }

        try:
            response = requests.get(
                "https://serpapi.com/search",
                params=params,
                timeout=10
            )
            results = response.json().get("organic_results", [])
            
            # Log API usage (for cost tracking)
            logger.info(
                f"SerpAPI Usage - Results: {len(results)}, "
                f"Query: {query[:50]}..."
            )
            
            return "\n".join(
                [f"{r['title']}: {r['snippet']}" for r in results[:3]]
            )

        except Exception as e:
            logger.error("Real-time search failed: %s", e)
            return ""
    
    def generate_rag_response(self, query: str, context: str, real_time_context: str) -> str:
        """Generate a natural answer using KB context (RAG).
        
        Args:
            query: User's company-related question
            context: Relevant content retrieved from KB
            real_time_context: Real-time search results from ZURU's official website
        
        Returns:
            Natural, concise answer based on KB context and real-time context
        """
        if not context:
            return f"No specific information found for: '{query}'. Please check the company intranet or contact HR/Engineering."
        
        prompt = f"""
            You are ZURU Melon's company assistant. Answer the user's question ONLY using the provided context.
            Do NOT use any external knowledge, do NOT make up information, and do NOT include irrelevant content.
            
            Guidelines:
            1. Answer clearly and concisely (under 300 words)
            2. Use natural, conversational language (avoid just copying text)
            3. If the context doesn't cover the question, use additional information from real-time search results to answer it, otherwise do not include any information from real-time search results.
            4. If the both context and real-time information cannot answer the question, respond with "Sorry, I don't have enough information to answer this question."
            5. Maintain ZURU's professional tone
            
            Context:
            {context}
            
            Additional Real-Time Information (if context couldn't answer the question):
            {real_time_context}
            
            User Question: {query}
        """

        payload = {
            "model": "openai/gpt-5.2",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 300,
            "temperature": 0.3,
            "top_p": 0.9
        }

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=20
            )
            response.raise_for_status()
            data = response.json()
            answer = data["choices"][0]["message"]["content"].strip()
            
            logger.info(
                f"RAG API Usage - Tokens: {data['usage']['total_tokens']}, "
                f"Query: {query[:50]}..."
            )
            return answer
        except requests.exceptions.RequestException as e:
            logger.error(f"RAG generation failed: {str(e)}")
            return f"\n\n{context}"