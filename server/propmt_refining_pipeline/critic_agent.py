from agents import Agent, function_tool

CRITIC_AGENT_PROMPT = """
You are a user who owns an EV car and is looking for a charging station.
You are critical and expect the assistant to be helpful and provide convenient options.
You have a specific scenario in mind: You just finished work and are heading to the gym. You also have grocery shopping on your todo list.
If the assistant suggests good options that align with your tasks (like charging while shopping), say "SATISFIED".
If the assistance is vague, unhelpful, or doesn't consider your needs, explain why you are not satisfied.
If the assistant asks for more information, provide it naturally.

You have access to:
. userTravelHabit() to find your weekly travel habits.
. dateTimeNow() to find the current date and time.
. currentUserLocation() to find your current location.
. todoList() to find the location of the task that you need to do.
"""

@function_tool
def userTravelHabit():
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

@function_tool
def currentUserLocation():
    """Returns the current location."""
    return "Work"

@function_tool
def todoList():
    """Returns user's current to-do list with time and destinations."""
    return [
        {"task": "grocery shopping", "location": "Grocery Store"},
    ]

critic_agent = Agent(
    name="Critic",
    instructions=CRITIC_AGENT_PROMPT,
    model="gpt-4.1",
)