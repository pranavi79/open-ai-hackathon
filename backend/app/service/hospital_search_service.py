from agents import Runner
from backend.app.agents.hospital_finder_agent import hospital_finder_agent
from backend.app.models.accident_report import AccidentReport
from backend.app.models.hospital_info import HospitalInfo
from backend.app.models.location_context import LocationContext
from backend.app.service.contact_agent_service import contact_agent_service

async def hospital_search_service(payload: AccidentReport, location_context: LocationContext) -> HospitalInfo:
    try:
        result = await Runner.run(
            hospital_finder_agent, 
            context=location_context,
            prompt=f"Imagine you're a first trauma responder Find the best hospital near location {payload.location} for an accident of type {payload.accident_type}.Accident details: {payload.details}").then(
                contact_agent_service(result.final_output_as(AccidentReport))
            )
        return result.final_output_as(AccidentReport)
    
    except Exception as e:
        raise Exception(f'hospital_search_service threw an exception {e}')
    