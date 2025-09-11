import asyncio
from agents import Agent, Runner
from agents.extensions.models.litellm_provider import LitellmProvider
from backend.app.core.config import OLLAMA_MODEL
from backend.app.tools.calling_tool import calling_tool

contact_agent = Agent(
    name="Contact Agent",
    instructions="""
    You are responsible for calling the best hospital near the accident location using the phone number.
    Provide a concise, polite, and complete message including the type of accident, exact location, and any relevant details.
    """,
    output_type=None,
    tools=[calling_tool],
    model=LitellmProvider().get_model(f'ollama_chat/{OLLAMA_MODEL}')
)

async def main():
    result = await Runner.run(
        contact_agent,
        "Call +918287880314 and inform about a major accident at Ananta Tech Park, Bangalore."
    )
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())