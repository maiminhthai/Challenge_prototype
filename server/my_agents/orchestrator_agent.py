from agents import Agent
from my_agents.driving_coach_agent import driving_coach_agent
from my_agents.charging_station_agent import charging_station_agent

orchestrator_agent = Agent(
    name="Orchestrator Agent",
    instructions="You determine which agent to use based on the user's query",
    handoffs=[driving_coach_agent, charging_station_agent],
    model="gpt-4o-mini",
)
