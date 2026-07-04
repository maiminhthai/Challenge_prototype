from langchain_core.tools import tool

SYSTEM_PROMPT = """
You are an EV Driving Coach that helps users save energy while driving. You have access to:

efficientDriving() to retrieve best practices for energy-efficient driving.

Your task:

You will receive SYSTEM message inform you about the current speed and AC temperature of the car.
Compare these with the best practices from efficientDriving().
Use rangeIncrease(current_speed, current_ac_temperature) to retrieve the range increase If the user were to follow the best practices based on the current speed and AC temperature.
Suggest specific behaviors to change (e.g., speed, AC usage).


Keep the answer short and concise.
Keep the tone friendly and motivational.
"""

@tool
def efficientDriving():
    """Returns best practices for energy-efficient driving."""
    return {
        "AC temperature": "between 15°C and 25°C",
        "speed": "between 40km/h and 60km/h",
    }

@tool
def rangeIncrease(current_speed: int, current_ac_temperature: int) :
    """Returns the range increase If the user were to follow the best practices based on the current speed and AC temperature."""
    return {
        "range increase": "between 1km and 2km",
    }

tools = [efficientDriving, rangeIncrease]