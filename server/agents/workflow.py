from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.runtime import get_runtime
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv

load_dotenv()

@tool
def weather(city: str) -> str:
    """Check the weather in a given city."""
    # Dummy implementation for illustration
    return f"The weather in {city} is sunny with a high of 25°C."

SYSTEM_PROMPT = "you are a comedian. When user asks for weather, use the weather tool to get the info."

config = {"configurable": {"thread_id": "1"}}

agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[weather],
    system_prompt=SYSTEM_PROMPT,
    checkpointer=InMemorySaver()
)