"""Settings Module - Central configuration for the system.

This module loads and validates system settings from environment
variables, adhering to ZURU Melon's configuration standards.
"""

from dataclasses import dataclass
import os
from typing import Optional

@dataclass
class Settings:
    """System settings for the company assistant.

    Attributes:
        openrouter_api_key: API key for OpenRouter
        openrouter_base_url: Base URL for OpenRouter API
        kb_path: Path to local knowledge base (Markdown files)
        block_harmful_content: Whether to block harmful content
        log_queries: Whether to log user queries
    """
    # OpenRouter Configuration
    openrouter_api_key: Optional[str] = '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'
    openrouter_base_url: str = "https://openrouter.ai/api/v1"

    # SerPAPI Configuration
    serp_api_key: Optional[str] = "8eda15dd156eb647d1eb7770464df25c679e605be451464042c6507a04c1fd60"
    
    # Knowledge Base Configuration
    kb_path: str = "../knowledge_base"

    # Compliance Configuration
    block_harmful_content: bool = True
    log_queries: bool = False

    def __post_init__(self) -> None:
        """Load settings from environment variables after initialization."""
        # Load OpenRouter settings
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY", self.openrouter_api_key)
        self.openrouter_base_url = os.getenv("OPENROUTER_BASE_URL", self.openrouter_base_url)

        # Load SerPAPI settings
        self.serp_api_key = os.getenv('SERP_API_KEY', self.serp_api_key)
        
        # Load KB path
        self.kb_path = os.getenv("KB_PATH", self.kb_path)

        # Load compliance settings
        block_harmful = os.getenv("BLOCK_HARMFUL_CONTENT", str(self.block_harmful_content))
        self.block_harmful_content = block_harmful.lower() == "true"

        log_queries = os.getenv("LOG_QUERIES", str(self.log_queries))
        self.log_queries = log_queries.lower() == "true"

        # Validate required settings
        self._validate()

    def _validate(self) -> None:
        """Validate critical settings."""
        # Check KB path exists
        if not os.path.exists(self.kb_path):
            raise NotADirectoryError(f"Knowledge base path does not exist: {self.kb_path}")

        # Warn if OpenRouter API key is missing (but don't fail - allow fallback)
        if not self.openrouter_api_key:
            print("WARNING: OpenRouter API key not found. General knowledge queries will not work.")