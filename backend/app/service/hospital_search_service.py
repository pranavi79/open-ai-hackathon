from agents import Runner
from backend.app.agents.hospital_finder_agent import hospital_finder_agent
from backend.app.models.accident_report import AccidentReport
from backend.app.models.hospital_info import HospitalInfo
from backend.app.models.location_context import LocationContext
from backend.app.service.contact_agent_service import contact_agent_service

async def hospital_search_service(payload: AccidentReport, location_context: LocationContext) -> HospitalInfo:
    try:
        result =await Runner.run(
            hospital_finder_agent, 
            context=location_context,
            input=f'''
            "You are a first responder at the scene of a road accident. "
            "The patient has {payload.details} as a {payload.accident_type} accident. "
            "Find the nearest hospital to the given location latitude={location_context.latitude}, longitude={location_context.longitude} and return only a JSON object with: "
            "name, address, rating, user_ratings_total, and phone_number."
            ''')
        contact_agent_service(result.final_output_as(AccidentReport))
        return result.final_output_as(AccidentReport)
    
    except Exception as e:
        raise Exception(f'hospital_search_service threw an exception {e}')
    