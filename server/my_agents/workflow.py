from agents.voice import AudioInput, VoicePipeline,  SingleAgentVoiceWorkflow
from my_agents.orchestrator_agent import orchestrator_agent

workflow = SingleAgentVoiceWorkflow(
    agent=orchestrator_agent,
)

voice_pipeline = VoicePipeline(workflow=workflow)

async def get_voice_response(data):
    audio_input = AudioInput(buffer=data)
    result = await voice_pipeline.run(audio_input)
    audio_output = []
    async for event in result.stream():
        if event.type == "voice_stream_event_audio":
            audio_output.append(event.data)
    return audio_output