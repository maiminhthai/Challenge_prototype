from agents import Agent, function_tool, WebSearchTool
from my_agents.driving_coach_agent import driving_coach_agent
from my_agents.charging_station_agent import charging_station_agent
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions
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

SYSTEM_PROMPT = """
You are an in-car assistant that answer user's general questions so be nice and friendly.
When you receive the message "SYSTEM: START" greet the user.

You have access to:

. userTravelHabits() to find the user's weekly travel habits.
. dateTimeNow() to find the current date and time.
. currentUserLocation() to find the current user location.
. WebSearchTool() to search the web.
. nearby(address: str, query: str) to find points of interest (e.g supermarkets, restaurants, etc.) close to the given address.
. findStation(query: str, currentLocation: str) to find points of interest (e.g supermarkets, restaurants, etc.) close to the current location.

When a question is related to driving efficiency or finding EV charging stations,
you should hand off the conversation to the appropriate specialist agent:
- driving_coach_agent for driving efficiency advice.
- charging_station_agent for finding EV charging stations.
"""

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

orchestrator_agent = Agent(
    name="Orchestrator Agent",
    instructions=prompt_with_handoff_instructions(SYSTEM_PROMPT),
    handoffs=[driving_coach_agent, charging_station_agent],
    tools=[userTravelHabits, dateTimeNow, currentUserLocation, nearby, findStation, WebSearchTool()],
    model="gpt-5",
)

