from agents import Runner
from backend.app.agents.hospital_finder_agent import hospital_finder_agent
from backend.app.models.accident_report import AccidentReport
from backend.app.models.hospital_info import HospitalInfo
from backend.app.models.location_context import LocationContext
from backend.app.service.contact_agent_service import contact_agent_service

async def hospital_search_service(payload: AccidentReport, location_context: LocationContext) -> AccidentReport:
    try:
        # Find the best hospital near the accident location
        hospital_result = await Runner.run(
            hospital_finder_agent, 
            context=location_context,
            prompt=f"Find the best hospital near location {payload.location} for an accident of type {payload.accident_type}. Accident details: {payload.details}"
        )
        
        best_hospital = hospital_result.final_output_as(HospitalInfo)
        
        # If it's a major trauma, contact the hospital
        if payload.accident_type == "major trauma" and best_hospital.phone_number:
            await contact_agent_service(best_hospital, payload)
        
        return payload
    
    except Exception as e:
        raise Exception(f'hospital_search_service threw an exception {e}')
    