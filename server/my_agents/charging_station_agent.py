from agents import Agent, function_tool, AgentHooks, RunContextWrapper, WebSearchTool


CHARGING_STATION_AGENT_PROMPT = """
You are a navigation assistant that helps users find EV charging stations based on their needs. Be nice and friendly.

If you receive a message from the SYSTEM, warning that the user's car needs charging, first you need to warn the user that his car needs charging.

You have acces to:

fastestStation() to find the charging station closest to the user's destination.
todoList() to find the location of the task that user need to do.
stationCloseTo() to find the charging station close to the location of the task.

Your task:

Find possible charging stations for the user.


Answer with the station name, address, distance and the reason why this station is chosen.
"""

# @function_tool
# def userProfile():
#     """Returns user's habitual routes and times."""
#     return {
#         "Monday": ["Home to Work (8 AM)", "Work to Gym (6 PM)"],
#         "Tuesday": ["Home to Work (8 AM)", "Work to Grocery Store (6 PM)"],
#         "Wednesday": ["Home to Work (8 AM)", "Work to Friend's House (6 PM)"],
#         "Thursday": ["Home to Work (8 AM)", "Work to Gym (6 PM)"],
#         "Friday": ["Home to Work (8 AM)", "Work to Restaurant (7 PM)"],
#         "Saturday": ["Home to Mall (11 AM)", "Mall to Home (4 PM)"],
#         "Sunday": ["Home to Park (10 AM)", "Park to Home (3 PM)"],
#     }

@function_tool
def todoList():
    """Returns user's current to-do list with time and destinations."""
    return [
        {"task": "Grocery Shopping", "location": "Grocery Store"},
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
        "Cinema": {"name": "MovieCharge Hub", "address": "606 Movie Ave", "distance": "0.9 miles"},
    }
    return stations.get(location, {"name": "Unknown", "address": "N/A", "distance": "N/A"})

@function_tool
def fastestStation(destination: str):
    """The least deviate charging station with respect to direction to a destination."""
    stations = {
        "Grocery Store": {"name": "GreenCharge Station", "address": "123 Green St", "distance": "0.5 miles"},
        "Dry Cleaners": {"name": "EcoCharge Hub", "address": "456 Eco Rd", "distance": "0.3 miles"},
        "Friend's House": {"name": "FastCharge Point", "address": "789 Fast Ln", "distance": "1.0 miles"},
        "Work": {"name": "OfficeCharge Spot", "address": "101 Work Ave", "distance": "0.2 miles"},
        "Gym": {"name": "FitCharge Center", "address": "202 Gym Blvd", "distance": "0.4 miles"},
        "Restaurant": {"name": "DineCharge Station", "address": "303 Food Ct", "distance": "0.6 miles"},
        "Mall": {"name": "ShopCharge Hub", "address": "404 Mall Dr", "distance": "0.7 miles"},
        "Park": {"name": "NatureCharge Point", "address": "505 Park St", "distance": "0.8 miles"},
        "Cinema": {"name": "MovieCharge Hub", "address": "606 Movie Ave", "distance": "0.9 miles"},
    }
    return stations.get(destination, {"name": "Unknown", "address": "N/A", "distance": "N/A"})

# @function_tool
# def dateTimeNow():
#     """Returns the current date and time."""
#     return "Tuesday, 5:42 PM"

#---Uncomment to enable tool usage logging---
# class MyHooks(AgentHooks):
#     async def on_tool_start(self, context: RunContextWrapper, agent: Agent, tool) -> None:
#         print(f"{agent.name} - {tool}")
# myHooks = MyHooks()

charging_station_agent = Agent(
    name="Charging Station Expert",
    handoff_description="Specialist agent for finding charging stations",
    instructions=CHARGING_STATION_AGENT_PROMPT,
    tools=[stationCloseTo, fastestStation, todoList, WebSearchTool()],
    model="gpt-4.1-mini",
    #hooks=myHooks,
)
