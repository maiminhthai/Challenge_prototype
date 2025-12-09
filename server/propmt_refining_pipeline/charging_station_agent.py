from agents import Agent, function_tool, AgentHooks, RunContextWrapper, WebSearchTool


CHARGING_STATION_AGENT_PROMPT = """
You are a navigation assistant that helps users find EV charging stations based on their needs. Be nice and friendly.

If you receive a message from the SYSTEM, warning that the user's car needs charging, first you need to warn the user that his car needs charging.

Assume that the type of charger is irrelevant and user's car can charge at any station.

You have acces to:

. fastestStation(currentLocation: str, destination: str) to find the charging station that is the least deviate from the direction to the destination.
. todoList() to find the location of the task that user need to do.
. stationCloseTo(location: str) to find the charging station close to a location.
. userTravelHabit() to find the user's weekly travel habits.
. dateTimeNow() to find the current date and time.
. currentUserLocation() to find the current user location.

Your task:

EV car take very long time to charge. Your task is to help user save time by finding chargings station that are the most convinient for them.
First find out is there anything that the user need to do.
Then findout if there is a station that allow user to charge while doing this task.

Suggest a few options. Answer with the station name, address, distance and the reason why this station is chosen.
"""

@function_tool
def todoList():
    """Returns user's current to-do list with time and destinations."""
    return [
        {"task": "grocery shopping", "location": "Grocery Store"},
    ]

@function_tool
def stationCloseTo(location: str):
    """Finds a charging station close to the given location."""
    stations = {
        "Grocery Store": {"name": "GreenCharge Station", "address": "123 Green St", "distance": "0.5 miles", "charging time": "45 minutes"},
        "Dry Cleaners": {"name": "EcoCharge Hub", "address": "456 Eco Rd", "distance": "0.3 miles", "charging time": "45 minutes"},
        "Friend's House": {"name": "FastCharge Point", "address": "789 Fast Ln", "distance": "1.0 miles", "charging time": "45 minutes"},
        "Work": {"name": "OfficeCharge Spot", "address": "101 Work Ave", "distance": "0.2 miles", "charging time": "45 minutes"},
        "Gym": {"name": "FitCharge Center", "address": "202 Gym Blvd", "distance": "0.4 miles", "charging time": "45 minutes"},
        "Restaurant": {"name": "DineCharge Station", "address": "303 Food Ct", "distance": "0.6 miles", "charging time": "45 minutes"},
        "Mall": {"name": "ShopCharge Hub", "address": "404 Mall Dr", "distance": "0.7 miles", "charging time": "45 minutes"},
        "Park": {"name": "NatureCharge Point", "address": "505 Park St", "distance": "0.8 miles", "charging time": "45 minutes"},
        "Cinema": {"name": "MovieCharge Hub", "address": "606 Movie Ave", "distance": "0.9 miles", "charging time": "45 minutes"},
    }
    return stations.get(location, {"name": "Unknown", "address": "N/A", "distance": "N/A", "charging time": "N/A"})

@function_tool
def fastestStation(currentLocation: str, destination: str):
    """The least deviate charging station with respect to direction to a destination."""
    stations = {
        "work": {
            "gym": {
                "name": "FastCharge Point",
                "address": "123 Fast St",
                "distance": "0.5 miles",
                "charging time": "25 minutes",
            }
        }
    }
    return stations.get(currentLocation, {"name": "Unknown", "address": "N/A", "distance": "N/A"}).get(destination, {"name": "Unknown", "address": "N/A", "distance": "N/A"})

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
    """Returns the current user location."""
    return "Work"

#---Uncomment to enable tool usage logging---
# class MyHooks(AgentHooks):
#     async def on_tool_start(self, context: RunContextWrapper, agent: Agent, tool) -> None:
#         print(f"{agent.name} - {tool}")
# myHooks = MyHooks()

charging_station_agent = Agent(
    name="Charging Station Expert",
    handoff_description="Specialist agent for finding charging stations",
    instructions=CHARGING_STATION_AGENT_PROMPT,
    tools=[stationCloseTo, fastestStation, todoList, userTravelHabit, dateTimeNow, currentUserLocation, WebSearchTool()],
    model="gpt-4.1-mini",
    #hooks=myHooks,
)
