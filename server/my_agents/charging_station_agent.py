from agents import Agent, function_tool, AgentHooks, RunContextWrapper, WebSearchTool
from my_agents.scraper import scrape_google_maps, scrape_nearby 

HOME = "Via Trana, 19, 10138 Torino TO"
WORK = "Corso Duca degli Abruzzi, 24, 10129 Torino TO"
GYM = "C.so Francesco Ferrucci, 112, 10141 Torino TO"
MALL = "Via Ermanno Fenoglietti, 15, 10126 Torino TO"
PARK = "Corso Massimo d'Azeglio, 10126 Torino TO"
# Routes
homeToWorkRoute = {
    "description": "Home to Work",
    "start_time": "8 AM",
    "end_time": "9 AM",
    "start_location": HOME,
    "end_location": WORK
}

workToGymRoute = {
    "description": "Work to Gym",
    "start_time": "6 PM",
    "end_time": "7:30 PM",
    "start_location": WORK,
    "end_location": GYM
}

gymToHomeRoute = {
    "description": "Gym to Home",
    "start_time": "8:30 PM",
    "end_time": "9 PM",
    "start_location": GYM,
    "end_location": HOME
}

homeToMallRoute = {
    "description": "Home to Mall",
    "start_time": "10 AM",
    "end_time": "11 AM",
    "start_location": HOME,
    "end_location": MALL
}

mallToHomeRoute = {
    "description": "Mall to Home",
    "start_time": "11 AM",
    "end_time": "12 PM",
    "start_location": MALL,
    "end_location": HOME
}

homeToParkRoute = {
    "description": "Home to Park",
    "start_time": "12 PM",
    "end_time": "1 PM",
    "start_location": HOME,
    "end_location": PARK
}

parkToHomeRoute = {
    "description": "Park to Home",
    "start_time": "1 PM",
    "end_time": "2 PM",
    "start_location": PARK,
    "end_location": HOME
}

CHARGING_STATION_AGENT_PROMPT = """
You are an intelligent EV Charging Assistant. Your goal is to find the most convenient charging station for the user based on their current context, such as their todo list, current location, time of day, and travel habits.

You have access to the following tools:

1. todoList() -> str
   Returns the tasks the user needs to complete (e.g., "buy groceries", "go to gym").
2. userTravelHabit() -> dict
   Returns a dictionary of the user's weekly travel habits and predicted destinations based on time.
3. dateTimeNow() -> str
   Returns the current date and time.
4. currentUserLocation() -> str
   Returns the current address/location of the user.
5. nearby(address: str, query: str) -> list
   Finds points of interest (query) close to a specific address.
6. findStation(query: str, currentLocation: str) -> list
   Finds facilities matching the query (use "charging station") near the current location.

Use the following format:

Question: the input question from the user
Thought: you should always think about what to do next in a step-by-step manner
Action: the action to take, should be one of [todoList, userTravelHabit, dateTimeNow, currentUserLocation, nearby, findStation]
Observation: the result of the action
... (this Thought/Action/Observation process can repeat N times)
Thought: I now know the final answer
Action: Finish[the final answer]

Begin!

Question: I need to charge my car, can you find a spot?
Thought: I need to understand the user's current context to find a "convenient" spot. First, I should check the current date, time, and location.
Action: dateTimeNow()
Observation: Monday, 5:30 PM
Thought: Now I need to check the user's location.
Action: currentUserLocation()
Observation: 500 Market St, San Francisco
Thought: It is Monday evening. I should check the user's todo list to see if they have any errands to run while charging.
Action: todoList()
Observation: - Buy milk and eggs
- Pick up dry cleaning
Thought: The user needs to buy groceries ("Buy milk and eggs"). I should look for charging stations that also have a supermarket nearby. First, I will find charging stations near 500 Market St.
Action: findStation("charging station", "500 Market St, San Francisco")
Observation: ["Volta Charging (Station A)", "EVgo (Station B)", "ChargePoint (Station C)"]
Thought: Now I need to check which of these stations is close to a supermarket. I will check Station A first.
Action: nearby("Volta Charging (Station A)", "supermarket")
Observation: []
Thought: Station A has no supermarket nearby. Let me check Station B.
Action: nearby("EVgo (Station B)", "supermarket")
Observation: ["Whole Foods Market"]
Thought: Station B is close to a Whole Foods. This is convenient for the user's task to buy milk.
Action: Finish[I recommend the EVgo station (Station B). It is located right next to Whole Foods Market, so you can cross "Buy milk and eggs" off your list while you charge.]

Question: Find me a charger.
Thought: I need to determine the best location. First, I will check the time and location.
Action: dateTimeNow()
Observation: Friday, 9:00 PM
Thought: I will check the user's location.
Action: currentUserLocation()
Observation: Downtown Office Park
Thought: It is late on a Friday. I'll check the todo list to see if there are active tasks.
Action: todoList()
Observation: No pending tasks.
Thought: Since there are no tasks and it is late, the user might be heading home. I should check their travel habits to confirm their likely destination for Friday nights.
Action: userTravelHabit()
Observation: {"Friday 9 PM": "Home (123 Maple Drive)"}
Thought: The user is likely heading to "Home (123 Maple Drive)". A convenient charger would be one near their home so they can charge overnight. I will search for stations near 123 Maple Drive.
Action: findStation("charging station", "123 Maple Drive")
Observation: ["Tesla Supercharger (Station X)", "Blink Charging (Station Y)"]
Thought: Station X is available near the user's destination.
Action: Finish[Since you are likely heading home, the most convenient option is the Tesla Supercharger (Station X) near 123 Maple Drive.]

User's charger type is CSS
Give the final answer only.
Suggest at most 3 options.
Answer with the station name, address, distance and the reason why this station is chosen.
"""

@function_tool
def todoList():
    """Returns user's current to-do list."""
    return [
        {"task": "grocery shopping"},
    ]

@function_tool
async def nearby(address: str, query: str):
    """
    address: str: the address to find locations close to.
    query: str: the query to find locations according to.
    Return a list of locations according to the query (e.g supermarket, restaurant, etc.) that are close to the given address.
    Each location has the following format:
    {
        "Name": name,
        "Rating": rating,
        "URL": url,
        "Address": address, 
        "Phone": phone,
        "Website": website,
        "Charger Types": charger_types,
        "Route Time": route_time,
        "Route Distance": route_distance,
    }
    Some field can be an empty string if the information is not available.
    """
    print("calling scrape_nearby")
    return await scrape_nearby(address, query)

@function_tool
async def findStation(query: str, currentLocation: str):
    """
    query: str: the query to find locations according to.
    currentLocation: str: the current location of the user.
    Return a list of locations according to the query (e.g charging station, restaurant, etc.) close to the given location.
    Each location has the following format:
    {
        "Name": name,
        "Rating": rating,
        "URL": url,
        "Address": address, 
        "Phone": phone,
        "Website": website,
        "Charger Types": charger_types,
        "Route Time": route_time,
        "Route Distance": route_distance,
    }
    To find charging station use "charging station" as query.
    Some field can be an empty string if the information is not available.
    """
    print("calling scrape_google_maps")
    return await scrape_google_maps(query, currentLocation)

@function_tool
def userTravelHabits():
    """Returns user's habitual routes and times. In the format of a dictionary.
    The dictionary has the following format:
    {
        "Monday": [routes],
        "Tuesday": [routes],
        "Wednesday": [routes],
        "Thursday": [routes],
        "Friday": [routes],
        "Saturday": [routes],
        "Sunday": [routes],
    }
    The key is the day of the week and the value is a list of routes that the user usually takes on that day.
    routes has the following format:
    {
        "description": "description of the route",
        "start_time": "start time of the route",
        "end_time": "end time of the route",
        "start_location": "adress of the starting location of the route",
        "end_location": "adress of the ending location of the route"
    }
    """
    return {
        "Monday": [homeToWorkRoute, workToGymRoute, gymToHomeRoute],
        "Tuesday": [homeToWorkRoute, workToGymRoute, gymToHomeRoute],
        "Wednesday": [homeToWorkRoute, workToGymRoute, gymToHomeRoute],
        "Thursday": [homeToWorkRoute, workToGymRoute, gymToHomeRoute],
        "Friday": [homeToWorkRoute, workToGymRoute, gymToHomeRoute],
        "Saturday": [homeToMallRoute, mallToHomeRoute],
        "Sunday": [homeToParkRoute, parkToHomeRoute],
    }

@function_tool
def dateTimeNow():
    """Returns the current date and time."""
    return "Tuesday, 5:42 PM"

@function_tool
def currentUserLocation():
    """Returns the current user location."""
    return WORK

#---Uncomment to enable tool usage logging---
# class MyHooks(AgentHooks):
#     async def on_tool_start(self, context: RunContextWrapper, agent: Agent, tool) -> None:
#         print(f"{agent.name} - {tool}")
# myHooks = MyHooks()

charging_station_agent = Agent(
    name="Charging Station Expert",
    handoff_description="Specialist agent for finding charging stations",
    instructions=CHARGING_STATION_AGENT_PROMPT,
    tools=[findStation, nearby, todoList, userTravelHabits, dateTimeNow, currentUserLocation, WebSearchTool()],
    model="gpt-4.1-mini",
    #hooks=myHooks,
)
