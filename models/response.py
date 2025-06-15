from pydantic import BaseModel
from typing import List, Optional

class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    correct_answer: str
    explanation: Optional[str] = None

class Quiz(BaseModel):
    topic: str
    difficulty: str
    questions: List[QuizQuestion]

class QuizResponse(BaseModel):
    quiz: Quiz
