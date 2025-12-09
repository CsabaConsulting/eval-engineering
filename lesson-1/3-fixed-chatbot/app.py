import os

from galileo import galileo_context
from galileo import GalileoScorers
from galileo.config import GalileoPythonConfig
from galileo.log_streams import enable_metrics

from galileo.openai import openai
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Access a variable with a default value
project_name = os.getenv("GALILEO_PROJECT", "EvalsCourse")
print(f"project_name: {project_name}")
log_stream_name = os.getenv("GALILEO_LOG_STREAM", "HRChatbot")
print(f"log_stream_name: {log_stream_name}")

# Set the project and Log stream, these are created if they don't exist.
# You can also set these using the GALILEO_PROJECT and GALILEO_LOG_STREAM
# environment variables.
galileo_context.init(project=project_name, log_stream=log_stream_name)

# Enable context adherence for the project
enable_metrics(
    project_name=project_name,
    log_stream_name=log_stream_name,
    metrics=[GalileoScorers.context_adherence],
)

# Initialize the Galileo OpenAI client wrapper
client = openai.OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="your_dummy_api_key" # Ollama doesn't require a real key
)

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
Question:

I am in the UK. How many vacation days do I have this year?

When answering this question, use the following context:
- My employment contract states that I have 30 days of annual leave.
- I have already taken 18 days of vacation this year.
"""

# Send a request to the LLM
response = client.chat.completions.create(
    model="gpt-oss:20b",  # "gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ],
)

# Print the response
print(response.choices[0].message.content.strip())

# Show Galileo information after the response
config = GalileoPythonConfig.get()
logger = galileo_context.get_logger_instance()
project_url = f"{config.console_url}project/{logger.project_id}"
log_stream_url = f"{project_url}/log-streams/{logger.log_stream_id}"

print()
print("🚀 GALILEO LOG INFORMATION:")
print(f"🔗 Project   : {project_url}")
print(f"📝 Log Stream: {log_stream_url}")
