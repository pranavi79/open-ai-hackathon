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
            f"{payload.request} at longitude {payload.longitude} and latitude {payload.latitude}").then(
        hospital_search_service(result, location_context=LocationContext(longitude=payload.longitude, latitude=payload.latitude)))
        return result.final_output_as(AccidentReport)
    
    except Exception as e:
        raise Exception(f'handle_question threw an exception {e}')
    