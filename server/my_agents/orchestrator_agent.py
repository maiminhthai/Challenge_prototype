from agents import Agent
from my_agents.driving_coach_agent import driving_coach_agent
from my_agents.charging_station_agent import charging_station_agent
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions

SYSTEM_PROMPT = """
You are an in-car assistant that answer user's general questions.  
When a question is related to driving efficiency or EV charging stations,
you should hand off the conversation to the appropriate specialist agent:
- driving_coach_agent for driving efficiency advice
- charging_station_agent for finding EV charging stations
"""

orchestrator_agent = Agent(
    name="Orchestrator Agent",
    instructions=prompt_with_handoff_instructions(SYSTEM_PROMPT),
    handoffs=[driving_coach_agent, charging_station_agent],
    model="gpt-4o-mini",
)
