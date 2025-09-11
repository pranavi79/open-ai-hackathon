import asyncio
from agents import Agent, Runner
from agents.extensions.models.litellm_provider import LitellmProvider
from backend.app.models.accident_report import AccidentReport
from backend.app.core.config import OLLAMA_MODEL


accident_response_agent = Agent(
    name="Accident Response Agent",
    instructions = '''
    You are a virtual assistant for reporting motor accidents.  
    Your job is to take a short accident description from the user and produce a **single JSON object** with the following fields:

    - "accident_type": either "minor" or "major trauma"
    - "first_aid_tips": a string with 2–3 short first aid steps
    - "location": the provided location (or "unknown" if not given)
    - "details": a short summary of the accident in plain English

    Rules:
    1. Always output a valid JSON object only. Do not include any explanations, greetings, or extra text.  
    2. Do not ask follow-up questions. Use "unknown" if information is missing.  
    3. End your response immediately after the JSON.  

    Example input:  
    "A motorbike fell, rider has small cuts on the leg."  

    Example output:  
    {
    "accident_type": "minor",
    "first_aid_tips": "Clean the wound with water, apply antiseptic, cover with a clean bandage.",
    "location": "unknown",
    "details": "Motorbike rider fell and suffered small cuts."
    }

    Do not continue the conversation. Always end with the JSON.
    ''',
    output_type=None,
    model=LitellmProvider().get_model(f'ollama_chat/{OLLAMA_MODEL}')
)

async def main():
    print(await Runner.run(
            accident_response_agent, 
            max_turns=1,
            input=f"I just witnessed a motor accident on the road near Ananta Tech Park in Bangalore. A bike collided with a car at the traffic signal. The rider fell down and has a deep cut on his leg, and he looks like he’s bleeding heavily. He seems conscious but in a lot of pain. The car driver is safe. Please help with first aid tips and find the nearest hospital quickly. at longitude 77.6107 and latitude 12.9345"))


if __name__ == "__main__":
    asyncio.run(main())


