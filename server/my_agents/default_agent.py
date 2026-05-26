from langchain_core.tools import tool
from my_agents.memory_manager import retrieve_user_memory


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
Keep the answer short and concise.

You have access to:

. userTravelHabits() to find the user's weekly travel habits.
. dateTimeNow() to find the current date and time.
. currentUserLocation() to find the current user location.
. getPersonalizedUserMemory(query) to find personalized user preferences, habits, or routines.

"""


@tool
async def userTravelHabits():
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

@tool
async def dateTimeNow():
    """Returns the current date and time."""
    return "Tuesday, 5:42 PM"

@tool
async def currentUserLocation():
    """Returns the current user location."""
    return WORK

@tool
async def todoList():
    """Returns user's current to-do list."""
    return [
        {"task": "grocery shopping"},
    ]

@tool
async def getPersonalizedUserMemory(query: str):
    """Retrieves user's preferences, habits, and routines from memory based on the query."""
    return retrieve_user_memory(query)

tools = [userTravelHabits, dateTimeNow, currentUserLocation, todoList, getPersonalizedUserMemory]