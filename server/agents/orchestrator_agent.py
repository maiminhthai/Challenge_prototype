from agents import Agent
from driving_coach_agent import history_tutor_agent
from trip_planning_expert_agent import math_tutor_agent

from dotenv import load_dotenv
load_dotenv()

triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question",
    handoffs=[history_tutor_agent, math_tutor_agent],
    model="openai:gpt-4o-mini",
)

