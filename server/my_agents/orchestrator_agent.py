from agents import Agent, function_tool
from my_agents.driving_coach_agent import driving_coach_agent
from my_agents.charging_station_agent import charging_station_agent
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions

SYSTEM_PROMPT = """
You are an in-car assistant that answer user's general questions.

When you receive the message "SYSTEM: START", proceed as follow:
1. Check the current date and time using dateTimeNow().
2. Then check todoList() to infer upcoming destinations.
3. If no tasks are scheduled, infer the most probable destination from userProfile() based on the current day and time.
note: Remember that any event before current time has likely already been completed.
4. Great the user with a friendly message then ask him if the infered destination is correct.

When a question is related to driving efficiency or EV charging stations,
you should hand off the conversation to the appropriate specialist agent:
- driving_coach_agent for driving efficiency advice
- charging_station_agent for finding EV charging stations
"""

@function_tool
def userProfile():
    """Returns user's habitual routes and times."""
    return {
        "Monday": ["Home to Work (8 AM)", "Work to Gym (6 PM)"],
        "Tuesday": ["Home to Work (8 AM)", "Work to Grocery Store (6 PM)"],
        "Wednesday": ["Home to Work (8 AM)", "Work to Friend's House (6 PM)"],
        "Thursday": ["Home to Work (8 AM)", "Work to Gym (6 PM)"],
        "Friday": ["Home to Work (8 AM)", "Work to Restaurant (7 PM)"],
        "Saturday": ["Home to Mall (11 AM)", "Mall to Home (4 PM)"],
        "Sunday": ["Home to Park (10 AM)", "Park to Home (3 PM)"],
    }

@function_tool
def todoList():
    """Returns user's current to-do list with time and destinations."""
    return [
        {"task": "Grocery Shopping", "time": "6 PM", "location": "Grocery Store"},
        {"task": "Pick up Dry Cleaning", "time": "5 PM", "location": "Dry Cleaners"},
        {"task": "Visit Friend", "time": "7 PM", "location": "Friend's House"},
    ]

@function_tool
def dateTimeNow():
    """Returns the current date and time."""
    return "Tuesday, 5:42 PM"

orchestrator_agent = Agent(
    name="Orchestrator Agent",
    instructions=prompt_with_handoff_instructions(SYSTEM_PROMPT),
    handoffs=[driving_coach_agent, charging_station_agent],
    tools=[userProfile, todoList, dateTimeNow],
    model="gpt-4o-mini",
)

