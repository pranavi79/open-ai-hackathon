from agents import Runner
from backend.app.agents.contact_agent import contact_agent
from backend.app.models.hospital_info import HospitalInfo
from backend.app.models.accident_report import AccidentReport

async def contact_agent_service(hospital_info: HospitalInfo, accident_report: AccidentReport) -> str:
    try:
        result = await Runner.run(
            contact_agent, 
            prompt=f"""
            You are a virtual assistant acting as a first responder. 
            Call the hospital to report an emergency.

            Hospital Information:
            - Name: {hospital_info.name}
            - Address: {hospital_info.address}
            - Phone: {hospital_info.phone_number}

            Accident Details:
            - Accident Type: {accident_report.accident_type}
            - Location: {accident_report.location}
            - Description: {accident_report.details}
            - First Aid Given: {accident_report.first_aid_tips}

            Instructions:
            1. Call the hospital at {hospital_info.phone_number}
            2. Craft a concise, professional message for the hospital staff
            3. Include accident type, location, severity, and current status
            4. Request immediate medical assistance or guidance
            """
        )
        return result.final_output_as(str)
    
    except Exception as e:
        raise Exception(f'contact_agent_service threw an exception {e}')
    