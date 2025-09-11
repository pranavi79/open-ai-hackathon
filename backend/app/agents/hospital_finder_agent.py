import asyncio
from agents import Agent, Runner
from agents.extensions.models.litellm_provider import LitellmProvider
from openai_harmony import ToolDescription
from backend.app.core.config import OLLAMA_MODEL
from backend.app.tools.fetch_nearest_hospital import fetch_nearest_hospital
from backend.app.models.location_context import LocationContext

hospital_finder_agent = Agent(
    name="Hospital Finder Agent",
    instructions="""
    You are a trauma responder. Your job is to search for the nearest hospital to the accident
    return only the hospital info in JSON format with these fields, respond unknown if you don't have the answer:
    {
        "name": "string" or "unknown",
        "address": "string" or "unknown",
        "rating": "string" or "unknown",
        "user_ratings_total": "string" or "unknown",
        "phone_number": "string" or "unknown",
    }
    """,
    output_type=None,
    tools=[fetch_nearest_hospital],
    model=LitellmProvider().get_model(f'ollama_chat/{OLLAMA_MODEL}')
)

async def main():
    location_context = LocationContext(latitude="12.9345", longitude="77.6107")
    print(await Runner.run(
            hospital_finder_agent, 
            context=location_context,
            input=(
                "You are a first responder at the scene of a road accident. "
                "The patient has heavy bleeding and a deep cut, categorized as a minor accident. "
                "Find the nearest hospital to the given location latitude=12.9345, longitude=77.6107 and return only a JSON object with: "
                "name, address, rating, user_ratings_total, and phone_number."
            )
    ))


if __name__ == "__main__":
    asyncio.run(main())