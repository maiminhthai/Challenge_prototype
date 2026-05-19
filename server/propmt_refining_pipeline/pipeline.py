import asyncio
import os
import sys
from dotenv import load_dotenv
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

# Ensure the current directory is in python path to load local modules
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from charging_station_agent import CHARGING_STATION_AGENT_PROMPT, tools as charging_tools
from critic_agent import CRITIC_AGENT_PROMPT, tools as critic_tools

# Load Environment Variables
load_dotenv()

# Initialize NIM LLM
llm = ChatNVIDIA(model="meta/llama-3.1-70b-instruct")

# Initialize Agents with memory checkpoints
memory_charging = MemorySaver()
memory_critic = MemorySaver()

charging_agent = create_react_agent(
    llm, 
    tools=charging_tools, 
    prompt=CHARGING_STATION_AGENT_PROMPT, 
    checkpointer=memory_charging
)
critic_agent = create_react_agent(
    llm, 
    tools=critic_tools, 
    prompt=CRITIC_AGENT_PROMPT, 
    checkpointer=memory_critic
)

async def run_pipeline():
    charging_config = {"configurable": {"thread_id": "charging_session"}}
    critic_config = {"configurable": {"thread_id": "critic_session"}}
    
    # Initial trigger
    initial_message = "SYSTEM: Your battery is low."
    print(f"--- Iteration 0 ---")
    print(f"User (System): {initial_message}")
    
    # Get initial response from Charging Station Agent
    response = await charging_agent.ainvoke(
        {"messages": [{"role": "user", "content": initial_message}]},
        config=charging_config
    )
    agent_text = response["messages"][-1].content
    print(f"Agent: {agent_text}")
    
    conversation_log = [
        f"User (System): {initial_message}",
        f"Agent: {agent_text}"
    ]

    for i in range(1, 4):
        print(f"\n--- Iteration {i} ---")
        
        # Critic reacts to Agent's last message
        critic_msg = f"The assistant said: '{agent_text}'. Respond to it acting as the user."
        critic_response = await critic_agent.ainvoke(
            {"messages": [{"role": "user", "content": critic_msg}]},
            config=critic_config
        )
        critic_text = critic_response["messages"][-1].content
        print(f"Critic: {critic_text}")
        conversation_log.append(f"Critic: {critic_text}")
        
        if "SATISFIED" in critic_text:
            print("\nCritic is satisfied. Stopping.")
            break
            
        # Agent responds to Critic
        response = await charging_agent.ainvoke(
            {"messages": [{"role": "user", "content": critic_text}]},
            config=charging_config
        )
        agent_text = response["messages"][-1].content
        print(f"Agent: {agent_text}")
        conversation_log.append(f"Agent: {agent_text}")

    # Save to file
    with open(os.path.join(current_dir, "conversation_log.txt"), "w") as f:
        f.write("\n\n".join(conversation_log))
    print(f"\nConversation saved to {os.path.join(current_dir, 'conversation_log.txt')}")

if __name__ == "__main__":
    asyncio.run(run_pipeline())
