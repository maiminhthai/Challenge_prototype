from agents import Agent, function_tool
from my_agents.driving_coach_agent import driving_coach_agent
from my_agents.charging_station_agent import charging_station_agent
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions

SYSTEM_PROMPT = """
You are an in-car assistant that answer user's general questions so be nice and friendly.
Stick to the instructions and tools provided. 
Remember that any event before current time has likely already been completed.

When you receive the message "SYSTEM: START", proceed as follow:
1. Check the current date and time using dateTimeNow().
2. Infer the most probable destination from userProfile() based on the current day and time.
3. Great the user with a friendly message then ask him if the infered destination is correct.

When a question is related to driving efficiency or finding EV charging stations,
you should hand off the conversation to the appropriate specialist agent:
- driving_coach_agent for driving efficiency advice
- charging_station_agent for finding EV charging stations
"""

@function_tool
def userProfile():
    """Returns user's habitual routes and times."""
    return {
        "Monday": ["Home to Work (8 AM)", "Work to Gym (6 PM)"],
        "Tuesday": ["Home to Work (8 AM)", "Work to Gym (6 PM)"],
        "Wednesday": ["Home to Work (8 AM)", "Work to Gym (6 PM)"],
        "Thursday": ["Home to Work (8 AM)", "Work to Gym (6 PM)"],
        "Friday": ["Home to Work (8 AM)", "Work to Gym (6 PM)"],
        "Saturday": ["Home to Mall (11 AM)", "Mall to Home (4 PM)"],
        "Sunday": ["Home to Park (10 AM)", "Park to Home (3 PM)"],
    }

@function_tool
def dateTimeNow():
    """Returns the current date and time."""
    return "Tuesday, 5:42 PM"

orchestrator_agent = Agent(
    name="Orchestrator Agent",
    instructions=prompt_with_handoff_instructions(SYSTEM_PROMPT),
    handoffs=[driving_coach_agent, charging_station_agent],
    tools=[userProfile, dateTimeNow],
    model="gpt-4.1",
)

