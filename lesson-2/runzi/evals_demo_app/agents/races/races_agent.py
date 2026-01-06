import os

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI

from evals_demo_app.tools.race_finder import find_races

# Ollama configuration
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434/v1")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "gpt-oss:20b")

races_agent = create_agent(
    name="agent",
    tools=[find_races],
    model=ChatOpenAI(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL,
        api_key="ollama",  # Ollama doesn't require a real key
        name="races-agent"
    ),
    system_prompt="""
    You are a helpful race finder agent. Use the tools available to you to provide users with details
    about upcoming races.

    Provide information such as race name, date, location, distance, difficulty, terrain, and type.
    """,
)


@tool
def get_races(request: str) -> str:
    """Get race information based on user input.

    Use this to get details about upcoming races, including name, date, location, distance, difficulty, terrain, and type.

    Input: Natural language race request from the user, including all the details about what they are looking for.
    """
    result = races_agent.invoke({"messages": [{"role": "user", "content": request}]})
    return result["messages"][-1].text
