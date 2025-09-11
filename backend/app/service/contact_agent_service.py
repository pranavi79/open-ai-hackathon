from agents import Runner
from backend.app.agents.contact_agent import contact_agent
from backend.app.models.hospital_info import HospitalInfo

async def contact_agent_service(payload: HospitalInfo) -> str:
    try:
        result = await Runner.run(
            contact_agent, 
            prompt=f"""
            You are a virtual assistant acting as a first responder. 
            Based on the following accident details, find the **best hospital** nearby.

            Accident Details:
            - Accident Type: {payload.accident_type}
            - Location: {payload.location}
            - Description: {payload.details}

            Instructions:
            1. Use any available data to select the most suitable hospital.
            2. Include the hospital's name, address, and phone number (if available).
            3. Craft a concise message for the hospital, including accident type, location, and details.
            4. Ensure the output is clear, professional, and actionable.
            """
        )

        return "success"
    
    except Exception as e:
        raise Exception(f'contact_agent_service threw an exception {e}')
    