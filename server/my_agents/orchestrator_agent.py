from my_agents.driving_coach_agent import driving_coach_agent
from my_agents.charging_station_agent import charging_station_agent
from my_agents.default_agent import default_agent
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions
from agents import Agent


SYSTEM_PROMPT = """
You are an orchestrator agent that handoff the conversation to the appropriate specialist agent.
Do not attempt to answer directly, instead handoff the conversation to the appropriate specialist agent:
- driving_coach_agent for driving efficiency advice.
- charging_station_agent for finding EV charging stations.
- default_agent if the question is not related to driving efficiency or finding EV charging stations.
"""

orchestrator_agent = Agent(
    name="Orchestrator Agent",
    instructions=prompt_with_handoff_instructions(SYSTEM_PROMPT),
    handoffs=[driving_coach_agent, charging_station_agent, default_agent],
    model="gpt-5-nano",
)

