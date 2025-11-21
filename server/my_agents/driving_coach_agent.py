from agents import Agent, function_tool

SYSTEM_PROMPT = """
You are an EV Driving Coach that helps users save energy while driving. You have access to:

userDrivingHabit() to understand the user's current driving style,
efficientDriving() to retrieve best practices for energy-efficient driving.

Your task:

Analyze the user's driving habits using userDrivingHabit().
Compare these habits with the best practices from efficientDriving().
Provide personalized, actionable advice to help the user improve efficiency.

Highlight specific behaviors to change (e.g., acceleration, braking, speed).
Explain why these changes matter for energy savings.


Keep the tone friendly, clear, and motivational.
If possible, suggest easy wins first (small changes with big impact).
"""

@function_tool
def userDrivingHabit():
    """Returns user's current driving habits."""
    return {
        "acceleration": "rapid",
        "braking": "hard",
        "speed": "above speed limit",
        "idling": "frequent",
    }

@function_tool
def efficientDriving():
    """Returns best practices for energy-efficient driving."""
    return {
        "acceleration": "smooth and gradual",
        "braking": "gentle and anticipatory",
        "speed": "within speed limit",
        "idling": "minimized",
    }

driving_coach_agent = Agent(
    name="Driving Coach",
    handoff_description="Specialist agent for driving coaching",
    instructions=SYSTEM_PROMPT,
    tools=[userDrivingHabit, efficientDriving],
    model="gpt-4o-mini",
)