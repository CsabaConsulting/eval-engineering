import os

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI

from evals_demo_app.tools.shoe_finder import (
    recommend_shoes,
    get_shoe_images,
)

# Ollama configuration
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434/v1")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "gpt-oss:20b")

shoe_agent = create_agent(
    tools=[recommend_shoes, get_shoe_images],
    name="agent",
    model=ChatOpenAI(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL,
        api_key="ollama",  # Ollama doesn't require a real key
        name="shoe-finder-agent"
    ),
    system_prompt="""
    You are a helpful shoe recommendation agent. You assist users in finding shoes based on their preferences such as category, brand, intended use, width, and price. You can also provide image URLs for the recommended shoes.

    Use all the tools available to you to provide the best recommendations possible. These tools only
    provide details of brands we have available. Other brands are available outside of this system.
    """,
)


@tool
def get_shoe_information(request: str) -> str:
    """Get information and images for running shoes based on user input.

    Use this to get shoe recommendations and images, based off details such as category, brand, intended use, width, and price.

    Input: Natural language shoe request from the user, including all the details about what they are looking for, such as the type of shoe, brand preferences, and any specific features they need.
    """
    result = shoe_agent.invoke({"messages": [{"role": "user", "content": request}]})
    return result["messages"][-1].text
