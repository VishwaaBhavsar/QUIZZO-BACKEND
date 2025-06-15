from pydantic import BaseModel
from typing import List, Optional, Any, Union

class Question(BaseModel):
    question: str
    type: str  # "multiple-choice" or "true-false"
    options: Optional[List[str]] = None  # Only for multiple-choice
    correct_answer: Union[int, bool]  # Index for multiple-choice, boolean for true-false
    explanation: Optional[str] = None

class Quiz(BaseModel):
    questions: List[Question]
    estimated_time: int  # in minutes
    difficulty: str
    total_questions: int

class QuizResponse(BaseModel):
    success: bool
    data: Optional[Quiz] = None
    message: str

class VideoValidationResponse(BaseModel):
    valid: bool
    message: str
    transcript_length: Optional[int] = None