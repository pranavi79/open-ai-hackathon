import asyncio
from agents import Agent, Runner
from agents.extensions.models.litellm_provider import LitellmProvider
from backend.app.core.config import OLLAMA_MODEL
from backend.app.models.hospital_info import HospitalInfo
from backend.app.tools.fetch_nearest_hospital import fetch_nearest_hospital, LocationContext

hospital_finder_agent = Agent(
    name="Hospital Finder Agent",
    instructions="""
    You are responsible for finding the best hospital near the accident location.
    1. Use the `fetch_nearest_hospital` tool to get a list of nearby hospitals.
    2. Compare them based on highest rating and reasonable number of user reviews.
    3. Return only the single best hospital as the output.
    """,
    output_type=HospitalInfo,
    tools=[fetch_nearest_hospital],
    tool_use_behavior="stop_on_first_tool",
    model=LitellmProvider().get_model(f'ollama_chat/{OLLAMA_MODEL}')
)

async def main():
    location_context = LocationContext(latitude=12.9345, longitude=77.6107)
    print(await Runner.run(
            hospital_finder_agent, 
            context=location_context,
            prompt=f"Imagine you're a first trauma responder Find the best hospital near location (77.6107 , 12.9345) for an accident of type minor .Accident details: heavy bleeding and deep cut"))


if __name__ == "__main__":
    asyncio.run(main())