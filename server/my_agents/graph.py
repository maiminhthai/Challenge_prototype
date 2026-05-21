from typing import Literal
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

# Import agents
from my_agents.driving_coach_agent import SYSTEM_PROMPT as DRIVING_COACH_PROMPT, tools as driving_coach_tools
from my_agents.charging_station_agent import CHARGING_STATION_AGENT_PROMPT, tools as charging_station_tools
from my_agents.default_agent import SYSTEM_PROMPT as DEFAULT_PROMPT, tools as default_tools

llm = ChatNVIDIA(model="openai/gpt-oss-120b")

driving_coach_node = create_react_agent(
    llm,
    tools=driving_coach_tools,
    prompt=DRIVING_COACH_PROMPT
)

charging_station_node = create_react_agent(
    llm,
    tools=charging_station_tools,
    prompt=CHARGING_STATION_AGENT_PROMPT
)

default_node = create_react_agent(
    llm,
    tools=default_tools,
    prompt=DEFAULT_PROMPT
)

# Wrapper functions for the nodes since create_react_agent returns a compiled graph
async def run_driving_coach(state: MessagesState):
    result = await driving_coach_node.ainvoke(state)
    return {"messages": result["messages"][-1]}

async def run_charging_station(state: MessagesState):
    result = await charging_station_node.ainvoke(state)
    return {"messages": result["messages"][-1]}

async def run_default(state: MessagesState):
    result = await default_node.ainvoke(state)
    return {"messages": result["messages"][-1]}

# Orchestrator Model
orchestrator_llm = ChatNVIDIA(model="meta/llama-3.1-8b-instruct")

class Route(BaseModel):
    next_agent: Literal["driving_coach_agent", "charging_station_agent", "default_agent"] = Field(
        description="The next agent to route to based on the user's request."
    )

def orchestrator_router(state: MessagesState):
    prompt = """You are an orchestrator agent that hands off the conversation to the appropriate specialist agent.
- driving_coach_agent for driving efficiency advice.
- charging_station_agent for finding EV charging stations.
- default_agent if the question is not related to driving efficiency or finding EV charging stations.
Determine which agent should handle the user's latest request.
"""
    messages = [{"role": "system", "content": prompt}] + state["messages"]
    router = orchestrator_llm.with_structured_output(Route)
    response = router.invoke(messages)
    return response.next_agent

# Build the graph
builder = StateGraph(MessagesState)

builder.add_node("driving_coach_agent", run_driving_coach)
builder.add_node("charging_station_agent", run_charging_station)
builder.add_node("default_agent", run_default)

builder.add_conditional_edges(START, orchestrator_router)

builder.add_edge("driving_coach_agent", END)
builder.add_edge("charging_station_agent", END)
builder.add_edge("default_agent", END)

app = builder.compile()
