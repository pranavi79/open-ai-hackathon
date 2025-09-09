from agents import Agent

from backend.app.agents.contact_agent import contact_agent
from backend.app.agents.accident_response_agent import accident_response_agent


triage_agent = Agent(
    name="Triage Agent",
    instructions="""
    You are responsible for deciding how to route accident cases:
    1. Always start by using the Accident Response Agent.
    2. If JSON returned by Accident Response Agent is valid and contains suficient information, handoff to Hospital Finder Agent to find the nearest hospital .
    3. If the accident is "major trauma", hand off to the Contact Agent to call the nearest hospital.
    """,
    handoffs=[accident_response_agent, contact_agent],
)