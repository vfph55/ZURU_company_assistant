"""ZURU Company Assistant - CLI Entry Point.

This module provides a command-line interface for interacting with the
company assistant agent, handling user input, and displaying responses.
"""

import sys
from typing import NoReturn
from venv import logger
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.markdown import Markdown

from agent.query_classifier import QueryClassifier
from agent.compliance_filter import ComplianceFilter
from agent.kb_retriever import KbRetriever
from agent.external_search import ExternalSearch
from agent.response_generator import ResponseGenerator
from utils.env_loader import load_env
from config.settings import Settings
from requests.exceptions import RequestException
from utils.logger import get_logger

logger = get_logger(__name__)

# Initialize Rich console for formatted output
console = Console()

# Load environment variables and settings
load_env()
settings = Settings()

def display_welcome() -> None:
    """Display welcome message and instructions."""
    welcome_text = """
        # ZURU Melon Company Assistant
        Welcome to the official company assistant!

        You can ask:
        - Company questions
        - General knowledge questions

        Type 'exit' to quit, 'help' for more options.
    """
    console.print(Panel(Markdown(welcome_text), title="Welcome"))

def handle_user_query(query: str) -> str:
    """Process a single user query through the agent pipeline.

    Args:
        query: User input string

    Returns:
        Formatted response string
    """
    # Step 1: Check compliance (block harmful content first)
    compliance_filter = ComplianceFilter(settings)
    if not compliance_filter.is_allowed(query):
        return "This query violates ZURU Melon's ethical guidelines and cannot be processed."

    # Step 2: Classify query type
    classifier = QueryClassifier(settings)
    query_type = classifier.classify(query)

    # Step 3: Handle different query types
    if query_type == "ambiguous":
        return "Could you clarify your question? It's unclear if this is about company policy or general knowledge."
    elif query_type == "company":
        # First try to retrieve from local KB
        kb_retriever = KbRetriever(settings)
        relevant_context = kb_retriever.retrieve(query)
        external_search = ExternalSearch(settings)
        real_time_context = external_search.real_time_search(query)
        
        # Use RAG to generate a response based on KB context as primary source and real-time search as additional information source if KB context cannot answer the question. 
        relevant_context = external_search.generate_rag_response(query, relevant_context, real_time_context)
        
        # If the KB and real-time search cannot answer the question, perform a general knowledge search as a fallback
        failed_singal = "Sorry, I don't have enough information to answer this question."
        if relevant_context.strip() == failed_singal:
            relevant_context = external_search.search(query)
            query_type = "general"
    elif query_type == "general":
        external_search = ExternalSearch(settings)
        relevant_context = external_search.search(query)
    else:
        relevant_context = ""

    # Step 4: Generate final response
    response_generator = ResponseGenerator(settings)
    response = response_generator.generate(query, relevant_context, query_type)

    return response

def run_cli() -> NoReturn:
    """Run the CLI interface for the company assistant."""
    display_welcome()

    while True:
        # Get user input
        user_input = Prompt.ask("\n[bold blue]You[/bold blue]")

        # Handle exit command
        if user_input.lower() in ["exit", "quit", "q"]:
            console.print("\nThank you for using ZURU Melon Company Assistant!")
            sys.exit(0)

        # Handle help command
        if user_input.lower() == "help":
            help_text = """
                Available commands:
                - exit/quit/q: Exit the assistant
                - help: Show this help message
                - Any question: Ask about company policies, general knowledge, etc.
            """
            console.print(Panel(Markdown(help_text), title="Help"))
            continue

        # Process query and display response
        try:
            with console.status("[bold green]Processing your query...[/bold green]"):
                response = handle_user_query(user_input)
            
            console.print(Panel(response, title="[bold green]ZURU Assistant[/bold green]"))
        except ValueError as e:
            console.print(f"Invalid input: {e}", style="red")
        except RequestException:
            console.print("Network error. Please try again.", style="red")
        except Exception:
            logger.exception("Unhandled error in CLI loop")
            console.print("Unexpected internal error occurred.", style="red")
if __name__ == "__main__":
    run_cli()