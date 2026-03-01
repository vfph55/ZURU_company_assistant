"""Knowledge Base Retriever - Extracts relevant info from local files.

This module parses company Markdown documents, creates embeddings for semantic
search, and retrieves relevant content for company-related queries.
"""

from typing import List, Optional
from dataclasses import dataclass
import os
import glob
import markdown
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer, util

from utils.markdown_parser import parse_markdown_file
from config.settings import Settings
from utils.logger import get_logger

logger = get_logger(__name__)

@dataclass
class KbRetriever:
    """Retrieves relevant content from the local company knowledge base.

    Attributes:
        settings: System settings object
        model: Sentence-BERT model for embedding generation
        kb_embeddings: Precomputed embeddings for KB content
        kb_texts: Corresponding text chunks for embeddings
        kb_sources: Source file paths for text chunks
    """
    settings: Settings
    model: Optional[SentenceTransformer] = None
    kb_embeddings: Optional[List[List[float]]] = None
    kb_texts: Optional[List[str]] = None
    kb_sources: Optional[List[str]] = None

    def __post_init__(self) -> None:
        """Initialize embedding model and load KB content."""
        # Load Sentence-BERT model (lightweight, cost-efficient)
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        
        # Load and process knowledge base files
        self._load_knowledge_base()

    def _load_knowledge_base(self) -> None:
        """Load and parse all Markdown files in the KB directory."""
        self.kb_texts = []
        self.kb_sources = []

        # Get all Markdown files in the KB directory
        md_files = glob.glob(os.path.join(self.settings.kb_path, "*.md"))
        if not md_files:
            raise FileNotFoundError(f"No Markdown files found in KB path: {self.settings.kb_path}")

        # Parse each file into chunks
        for file_path in md_files:
            try:
                # Parse markdown file into text chunks (per section)
                chunks = parse_markdown_file(file_path)
                for chunk in chunks:
                    # Clean text (remove markdown formatting)
                    html = markdown.markdown(chunk)
                    clean_text = BeautifulSoup(html, "html.parser").get_text(strip=True)
                    
                    if clean_text and len(clean_text) > 20:  # Skip empty/short chunks
                        self.kb_texts.append(clean_text)
                        self.kb_sources.append(os.path.basename(file_path))
            except FileNotFoundError:
                logger.error("File not found: %s", file_path)
                continue
            except PermissionError:
                logger.error("No permission to read file: %s", file_path)
                continue
            except UnicodeDecodeError as e:
                logger.error("Encoding error while reading %s: %s", file_path, e)
                continue
            except ValueError as e:
                logger.error("Invalid markdown content in %s: %s", file_path, e)
                continue
            except (TypeError, AttributeError) as e:
                logger.error("Type/attribute error while parsing %s: %s", file_path, e)
                continue

        # Generate embeddings for all text chunks
        if self.kb_texts:
            self.kb_embeddings = self.model.encode(self.kb_texts, convert_to_tensor=True)
        else:
            self.kb_embeddings = None

    def retrieve(self, query: str, top_k: int = 5) -> str:
        """Retrieve relevant content from the KB for a given query.

        Args:
            query: User query string
            top_k: Number of top relevant chunks to retrieve

        Returns:
            Concatenated relevant content with source attribution
        """
        if self.kb_embeddings is None:
            return ""
        if not self.kb_texts:
            return ""

        # Generate embedding for query
        query_embedding = self.model.encode(query, convert_to_tensor=True)

        # Compute cosine similarity between query and KB chunks
        cos_scores = util.cos_sim(query_embedding, self.kb_embeddings)[0]
        top_results = cos_scores.topk(k=top_k)

        # Collect relevant chunks with sources
        relevant_content = []
        for score, idx in zip(top_results[0], top_results[1]):
            score_f = float(score.item())
            idx_i = int(idx.item())
            if score_f > 0.2:  # Minimum relevance threshold
                source = self.kb_sources[idx_i]
                text = self.kb_texts[idx_i]
                relevant_content.append(f"[Source: {source}]\n{text}\n")

        return "\n---\n".join(relevant_content)
   