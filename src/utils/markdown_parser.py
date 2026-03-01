"""Markdown Parser - Utility for parsing Markdown files into usable text chunks.

This module parses Markdown files (company docs) into section-based chunks
for efficient retrieval in the knowledge base.
"""

from typing import List
import os

def parse_markdown_file(file_path: str) -> List[str]:
    """Parse a Markdown file into section-based text chunks.

    Args:
        file_path: Path to the Markdown file

    Returns:
        List of text chunks (one per section)
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Markdown file not found: {file_path}")

    chunks = []
    current_chunk = []
    section_headers = ["#", "##", "###"]

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        stripped_line = line.strip()

        # Check if line is a section header
        if any(stripped_line.startswith(header) for header in section_headers):
            # Save current chunk if it has content
            if current_chunk:
                chunks.append("\n".join(current_chunk))
                current_chunk = []
        
        # Add line to current chunk (skip empty lines)
        if stripped_line:
            current_chunk.append(stripped_line)

    # Add the last chunk
    if current_chunk:
        chunks.append("\n".join(current_chunk))

    return chunks