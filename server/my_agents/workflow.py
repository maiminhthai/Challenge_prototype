from agents.voice import AudioInput, VoicePipeline,  SingleAgentVoiceWorkflow
from my_agents.orchestrator_agent import orchestrator_agent

workflow = SingleAgentVoiceWorkflow(
    name="In-Car Assistant Voice Workflow",
    agent=orchestrator_agent,
)

voice_pipeline = VoicePipeline(workflow=workflow)

