"""
LLM configuration module for switching between Ollama and OpenAI.

If OPENAI_API_KEY contains "_dummy_", uses Ollama; otherwise uses OpenAI.

Environment variables (can be set in .env file):
- OPENAI_API_KEY: If contains "_dummy_", uses Ollama; otherwise uses OpenAI
- OLLAMA_MODEL: Model to use with Ollama (default: gpt-oss:20b)
- OLLAMA_BASE_URL: Ollama server URL (default: http://localhost:11434/v1)
- OPENAI_MODEL: Model to use with OpenAI (default: gpt-4o-mini)
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
load_dotenv(override=True)


def get_api_key() -> str:
    """Get the OpenAI API key from environment."""
    return os.environ.get("OPENAI_API_KEY", "")


def use_ollama() -> bool:
    """Check if we should use Ollama based on the API key."""
    return "_dummy_" in get_api_key()


def get_llm_config() -> dict:
    """
    Get LLM configuration based on whether we're using Ollama or OpenAI.
    
    Returns a dict with model, base_url (if Ollama), and api_key (if Ollama).
    """
    if use_ollama():
        return {
            "model": os.environ.get("OLLAMA_MODEL", "gpt-oss:20b"),
            "base_url": os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
            "api_key": "ollama",
        }
    else:
        return {
            "model": os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        }


def create_chat_model(name: str) -> ChatOpenAI:
    """
    Create a ChatOpenAI instance configured for either Ollama or OpenAI.
    
    Args:
        name: The name to assign to this model instance.
    
    Returns:
        A configured ChatOpenAI instance.
    """
    config = get_llm_config()
    
    if use_ollama():
        print(f"Using Ollama at {config['base_url']} with model {config['model']}")
        return ChatOpenAI(
            model=config["model"],
            base_url=config["base_url"],
            api_key=config["api_key"],
            name=name,
        )
    else:
        print(f"Using OpenAI with model {config['model']}")
        return ChatOpenAI(
            model=config["model"],
            name=name,
        )

