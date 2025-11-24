from agents import Agent, function_tool, AgentHooks, RunContextWrapper


SYSTEM_PROMPT = """
You are a navigation assistant that helps users find EV charging stations based on both their travel habits and to-do list. You have access to:

. userProfile() for habitual routes and times,
. todoList() for current tasks and destinations,
. stationCloseTo(A) to find a charging station near a location A.
. dateTimeNow() to get the current date and time.

When the user's car needs charging, first check the current date and time using dateTimeNow().
Remember that any event before current time has likely already been completed.
Then check todoList() for upcoming destinations.
If no tasks are scheduled, infer the most probable destination from userProfile() based on the current day and time.
Then, use stationCloseTo() to find the nearest charging station to that location.
Respond with the station's name, address, and distance, and explain whether the choice was based on habits or tasks.
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
def stationCloseTo(location: str):
    """Finds a charging station close to the given location."""
    stations = {
        "Grocery Store": {"name": "GreenCharge Station", "address": "123 Green St", "distance": "0.5 miles"},
        "Dry Cleaners": {"name": "EcoCharge Hub", "address": "456 Eco Rd", "distance": "0.3 miles"},
        "Friend's House": {"name": "FastCharge Point", "address": "789 Fast Ln", "distance": "1.0 miles"},
        "Work": {"name": "OfficeCharge Spot", "address": "101 Work Ave", "distance": "0.2 miles"},
        "Gym": {"name": "FitCharge Center", "address": "202 Gym Blvd", "distance": "0.4 miles"},
        "Restaurant": {"name": "DineCharge Station", "address": "303 Food Ct", "distance": "0.6 miles"},
        "Mall": {"name": "ShopCharge Hub", "address": "404 Mall Dr", "distance": "0.7 miles"},
        "Park": {"name": "NatureCharge Point", "address": "505 Park St", "distance": "0.8 miles"},
    }
    return stations.get(location, {"name": "Unknown", "address": "N/A", "distance": "N/A"})

@function_tool
def dateTimeNow():
    """Returns the current date and time."""
    return "Tuesday, 5:42 PM"

#---Uncomment to enable tool usage logging---
# class MyHooks(AgentHooks):
#     async def on_tool_start(self, context: RunContextWrapper, agent: Agent, tool) -> None:
#         print(f"{agent.name} - {tool}")
# myHooks = MyHooks()

charging_station_agent = Agent(
    name="Charging Station Expert",
    handoff_description="Specialist agent for finding charging stations",
    instructions=SYSTEM_PROMPT,
    tools=[userProfile, todoList, stationCloseTo, dateTimeNow],
    model="gpt-4o-mini",
    #hooks=myHooks,
)
