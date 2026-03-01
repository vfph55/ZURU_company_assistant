"""Environment Loader - Utility for loading environment variables from .env file.

This module loads environment variables from a .env file into the OS environment.
"""

import os
from dotenv import load_dotenv

def load_env(env_file: str = ".env") -> None:
    """Load environment variables from a .env file.

    Args:
        env_file: Path to the .env file (default: .env)
    """
    if os.path.exists(env_file):
        load_dotenv(env_file)
        print(f"Loaded environment variables from {env_file}")
    else:
        print(f"Warning: {env_file} not found. Using system environment variables.")