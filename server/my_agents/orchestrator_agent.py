from agents import Agent
from my_agents.driving_coach_agent import history_tutor_agent
from my_agents.trip_planning_expert_agent import math_tutor_agent

triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question",
    handoffs=[history_tutor_agent, math_tutor_agent],
    model="openai:gpt-4o-mini",
)
