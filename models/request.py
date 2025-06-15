from pydantic import BaseModel
from typing import Optional

class QuizRequest(BaseModel):
    topic: str
    difficulty: str = "medium"
    question_count: int = 5
    question_type: str = "multiple-choice"
