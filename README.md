# EV Charging Assistant Prototype

This project is a prototype for an intelligent EV charging assistant. It consists of a Python Flask server with OpenAI agents and a React client.

## Setup

### Client
1. Navigate to the client directory:
   ```bash
   cd client
   ```
2. Install dependencies:
   ```bash
   npm install
   ```

### Server
1. Navigate to the server directory:
   ```bash
   cd server
   ```
2. Sync dependencies (using uv):
   ```bash
   uv sync
   ```

## Running the Project

You will need two terminal windows.

**Terminal 1 (Server):**
```bash
cd server
uv run main.py
```

**Terminal 2 (Client):**
```bash
cd client
npm run dev
```

## Project Overview

### Server
The server is built with Flask and Flask-SocketIO. It hosts several AI agents that interact to assist the user.

- **Main Entry Point**: `server/main.py` - Sets up the Flask app and SocketIO events.
- **Agents**: Located in `server/my_agents/`.
    - `charging_station_agent.py`: Expert agent for finding charging stations based on location, habits, and tasks.
    - `orchestrator_agent.py`: Manages the conversation flow.
    - `driving_coach_agent.py`: Agent for driving advice.

### Prompt Refining Pipeline
Included is a pipeline for refining the `charging_station_agent`'s prompt by simulating conversations with a critic.

- **Location**: `server/propmt_refining_pipeline/`
- **Components**:
    - `pipeline.py`: Script to run the conversation loop.
    - `critic_agent.py`: Simulates a user with specific needs to test the charging agent.
    - `conversation_log.txt`: Logs the interaction history which serves as few-shot examples for the agent.

### Travel Log
A module to generate synthetic user travel data, representing the user's travel habits to be used by the agents.

- **Location**: `server/travel_log/`
- **Components**:
    - `generate_travel_log.py`: Script to generate 3 months of trip data with realistic patterns (e.g., Home -> Work -> Gym on weekdays).
    - `travel_log.csv`: The generated dataset containing Date, Time, and Location info.

## Features
- **Voice Interaction**: Supports audio input/output (work in progress).
- **Context Awareness**: Agents have access to mock tools like `todoList`, `userTravelHabit`, etc.
- **Agent Evaluation**: Automated critique loop to improve agent responses.

## Changes compared to last week.
Instead of telling the agent exactly what to do, I give it the problem and a few question to guide it to reason through the problem.

```
EV car take very long time to charge. Your task is to help user save time by finding chargings station that are the most convinient for them.
First find out is there anything that the user need to do.
Then find out if there is a station that allow user to charge while doing this task.
```
Taken inspiration from Constitutional AI paper. I added a pipline where a critic agent acting as the user and the charging station agent providing responses. The critic agent will provide feedback to the charging station agent to improve its responses. These two run in a loop until the critic agent is satisfied with the charging station agent's responses. Then their converstion is saved to a file and used later in the prompt as few-shot examples for the charging station agent.

Why this approach?
- Refine the agent's responses to better align with user needs.
- No human in the loop. It can automatically run when user's habbits and preference changes.
- Adding a producer-critic loop directly during run time add more latency so by running it before and add it to the prompt as few-shot examples
provide a better compromize between latency and quality.

## Questions.
- Is this a good approach?
- Is there a better way to do this?