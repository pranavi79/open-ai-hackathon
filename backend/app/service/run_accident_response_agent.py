import json
from agents import Runner
from backend.app.agents.accident_response_agent import accident_response_agent
from backend.app.models.accident_report import AccidentReport
from backend.app.models.location_context import LocationContext
from backend.app.models.user_request import UserRequest
from backend.app.service.hospital_search_service import hospital_search_service

async def handle_question(payload: UserRequest) -> AccidentReport:
    try:
        result = await Runner.run(
            accident_response_agent, 
            f"{payload.request} at longitude {payload.longitude} and latitude {payload.latitude}")
        accident_report = result.final_output_as(AccidentReport)
        # pass to hospital search
        hospital_search_service(
            accident_report, 
            location_context=LocationContext(
                longitude=payload.longitude, 
                latitude=payload.latitude
            )
        ) 
        
        return accident_report
    
    except Exception as e:
        raise Exception(f'handle_question threw an exception {e}')
    