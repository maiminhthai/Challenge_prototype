# EV Charging Assistant Prototype

This project is a prototype for an intelligent EV charging assistant. It consists of a Python Flask server powered by **LangGraph** (with **NVIDIA NIM** for agent orchestration and reasoning) and a React client.

## Setup

### Prerequisites

Make sure you have `uv` installed to manage Python packages and environments easily.

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
2. Configure environment variables. Create a `.env` file in the `server` directory and add your API keys:
   ```env
   OPENAI_API_KEY=your-openai-api-key       # Used for STT and TTS models
   NVIDIA_API_KEY=your-nvidia-nim-api-key   # Used for ChatNVIDIA agent models
   ```
3. Sync dependencies (using uv):
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

The server is built with Flask and Flask-SocketIO. It uses a **LangGraph StateGraph** to orchestrate several AI agents powered by **NVIDIA NIM** models to assist the user.

- **Main Entry Point**: `server/main.py` - Sets up the Flask app and SocketIO events.
- **Workflow & Checkpointing**: `server/my_agents/workflow.py` - Compiles the LangGraph dynamically with `AsyncSqliteSaver` for persistent database checkpointing. Uses OpenAI `whisper-1` and `tts-1` for audio processing.
- **Orchestration**: `server/my_agents/graph.py` - Houses the central state graph and routing logic. An orchestrator node classifies the query and routes to the appropriate specialist agent using `meta/llama-3.1-8b-instruct`.
- **Agents**: Specialist agents are created using LangGraph's `create_react_agent` on `meta/llama-3.1-70b-instruct` with Langchain tools.
  - `charging_station_agent.py`: Specialist for finding charging stations based on location, habits, and tasks.
  - `driving_coach_agent.py`: Specialist for driving efficiency advice.
  - `default_agent.py`: Handles general queries.

### Prompt Refining Pipeline

Included is a pipeline for refining the `charging_station_agent`'s prompt by simulating conversations with a critic. This is also powered by NVIDIA NIM ChatNVIDIA LLMs.

- **Location**: `server/propmt_refining_pipeline/`
- **Components**:
  - `pipeline.py`: Script to run the conversation loop. Uses LangGraph `MemorySaver` to retain state.
  - `critic_agent.py`: Simulates a user with specific needs to test the charging agent.
  - `conversation_log.txt`: Logs the interaction history which serves as few-shot examples for the agent.

### Travel Log

A module to generate synthetic user travel data, representing the user's travel habits to be used by the agents.

- **Location**: `server/travel_log/`
- **Components**:
  - `generate_travel_log.py`: Script to generate 3 months of trip data with realistic patterns (e.g., Home -> Work -> Gym on weekdays).
  - `travel_log.csv`: The generated dataset containing Date, Time, and Location info.

## Features

- **LangGraph Orchestration**: Robust multi-agent design with structured conditional routing.
- **NVIDIA NIM LLMs**: Fast and powerful model reasoning using Llama 3.1 instruct models via NIM.
- **SQLite Persistence**: Automatically preserves thread conversation history via LangGraph checkpointing.
- **Voice Interaction**: Supports speech-to-text and text-to-speech interaction via OpenAI.
- **Context Awareness**: Agents have access to tools like `todoList`, `userTravelHabits`, etc.
- **Agent Evaluation**: Automated critique loop to improve agent responses.
