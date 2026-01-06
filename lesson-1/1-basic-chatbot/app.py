import os
from galileo.openai import openai
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Check if using Ollama (dummy key) or OpenAI (real key)
api_key = os.getenv("OPENAI_API_KEY", "")
use_ollama = "_dummy_" in api_key

if use_ollama:
    # Ollama configuration
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
    model = os.getenv("OLLAMA_MODEL", "gpt-oss:20b")
    client = openai.OpenAI(base_url=base_url, api_key=api_key)
    print(f"Using Ollama at {base_url} with model {model}")
else:
    # OpenAI configuration
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    client = openai.OpenAI()
    print(f"Using OpenAI with model {model}")

# Define a system prompt with guidance
system_prompt = """
You are a helpful HR assistant. Provide very clear, very short,
and very succinct answers to the user's questions based off their
employment contract and other criteria.

Just provide the details asked, avoiding any extra information
or explanations.
"""

# Define a user prompt with a question
user_prompt = """
I am in the UK. How many vacation days do I have this year?
"""

# Send a request to the LLM
response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
)

# Print the response
print(response.choices[0].message.content.strip())
