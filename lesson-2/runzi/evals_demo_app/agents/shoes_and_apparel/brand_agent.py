import os

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI

from evals_demo_app.tools.brand_info import (
    get_brand_info,
    get_brand_images,
)

# Ollama configuration
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434/v1")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "gpt-oss:20b")

brand_agent = create_agent(
    tools=[get_brand_info, get_brand_images],
    name="agent",
    model=ChatOpenAI(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL,
        api_key="ollama",  # Ollama doesn't require a real key
        name="brand-information-agent"
    ),
    system_prompt="""
    You are a helpful brand information agent. You can provide users with information about shoe and clothing
    brands including their name, slogan, story, and logos.

    Use all the tools available to you to provide the best recommendations possible. These tools only
    provide details of brands we have available. Other brands are available outside of this system.
    """,
)


@tool
def get_brand_information(request: str) -> str:
    """Get information and images for brands of running shoes and apparel based on user input.

    Use this to get brand recommendations and images, based off details such as category, brand, intended use, width, and price.

    Input: Natural language brand request from the user, including all the details about what they are looking for, such as the type of brand, brand preferences, and any specific features they need.
    """
    result = brand_agent.invoke({"messages": [{"role": "user", "content": request}]})
    return result["messages"][-1].text
