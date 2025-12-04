from agents import Agent, function_tool

SYSTEM_PROMPT = """
You are an EV Driving Coach that helps users save energy while driving. You have access to:

userDrivingHabit() to understand the user's driving habits during heavy traffic and low traffic,
efficientDriving() to retrieve best practices for energy-efficient driving.

Your task:

You will receive SYSTEM message inform you about the upcomming traffic condition.
Analyze the user's driving habits using userDrivingHabit() during heavy traffic and low traffic.
Compare these habits with the best practices from efficientDriving().

Inform user of upcoming traffic condition.
Suggest specific behaviors to change (e.g., acceleration, braking, speed).

Keep the answer short and concise.
Keep the tone friendly and motivational.
"""

@function_tool
def userDrivingHabit():
    """Returns user's current driving habits during heavy traffic and low traffic."""
    return {
        "heavy traffic": "acceleration: rapid, braking: hard",
        "low traffic": "speed: above limit",
    }

@function_tool
def efficientDriving():
    """Returns best practices for energy-efficient driving."""
    return {
        "acceleration": "smooth and gradual",
        "braking": "smoth braking",
        "speed": "within speed limit",
    }

driving_coach_agent = Agent(
    name="Driving Coach",
    handoff_description="Specialist agent for driving coaching",
    instructions=SYSTEM_PROMPT,
    tools=[userDrivingHabit, efficientDriving],
    model="gpt-4.1",
)