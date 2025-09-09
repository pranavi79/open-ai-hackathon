from fastapi import APIRouter, HTTPException

from backend.app.models.accident_report import AccidentReport
from backend.app.models.user_request import UserRequest
from backend.app.service.run_accident_response_agent import handle_question

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "This is your entry into open ai hackathon project"}

@router.post("/ask", response_model=AccidentReport)
async def ask_question(payload: UserRequest):
    try:
        return await handle_question(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))