from fastapi import APIRouter, HTTPException
from models.request import QuizRequest
from models.response import QuizResponse
from services.quiz_service import generate_quiz_logic

router = APIRouter()

@router.post("", response_model=QuizResponse)
async def generate_quiz(request: QuizRequest):
    return await generate_quiz_logic(request)
