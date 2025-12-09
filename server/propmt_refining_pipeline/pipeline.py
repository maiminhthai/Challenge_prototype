import asyncio
import os
from agents import Runner, OpenAIConversationsSession
import sys

# Ensure the server directory is in python path
current_dir = os.path.dirname(os.path.abspath(__file__))
server_dir = os.path.dirname(current_dir)
if server_dir not in sys.path:
    sys.path.append(server_dir)

from charging_station_agent import charging_station_agent
from critic_agent import critic_agent

# Get current directory

from dotenv import load_dotenv
# --- Load Environment Variables ---
load_dotenv()

async def run_pipeline():
    session = OpenAIConversationsSession()
    
    # Initial trigger
    initial_message = "SYSTEM: Your battery is low."
    print(f"--- Iteration 0 ---")
    print(f"User (System): {initial_message}")
    
    # Get initial response from Charging Station Agent
    agent_response = await Runner.run(charging_station_agent, initial_message, session=session)
    agent_text = agent_response.final_output
    print(f"Agent: {agent_text}")
    
    conversation_log = [
        f"User (System): {initial_message}",
        f"Agent: {agent_text}"
    ]

    for i in range(1, 4):
        print(f"\n--- Iteration {i} ---")
        
        # Critic reacts to Agent's last message
        critic_response = await Runner.run(critic_agent, f"The assistant said: '{agent_text}'. Respond to it acting as the user.", session=session)
        critic_text = critic_response.final_output
        print(f"Critic: {critic_text}")
        conversation_log.append(f"Critic: {critic_text}")
        
        if "SATISFIED" in critic_text:
            print("\nCritic is satisfied. Stopping.")
            break
            
        # Agent responds to Critic
        agent_response = await Runner.run(charging_station_agent, critic_text, session=session)
        agent_text = agent_response.final_output
        print(f"Agent: {agent_text}")
        conversation_log.append(f"Agent: {agent_text}")

    # Save to file
    with open(os.path.join(current_dir, "conversation_log.txt"), "w") as f:
        f.write("\n\n".join(conversation_log))
    print(f"\nConversation saved to {os.path.join(current_dir, 'conversation_log.txt')}")

if __name__ == "__main__":
    asyncio.run(run_pipeline())
