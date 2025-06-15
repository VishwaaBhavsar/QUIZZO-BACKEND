import json
import re
from fastapi import HTTPException
from models.request import QuizRequest
from models.response import Quiz, QuizQuestion, QuizResponse
from services.ai_service import get_gemini_model_response

def clean_json_response(text: str) -> str:
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*$', '', text)
    match = re.search(r'\{.*\}', text, re.DOTALL)
    return match.group(0) if match else text.strip()

def generate_quiz_prompt(topic, difficulty, question_count, question_type):
    difficulty_map = {
        "easy": "basic concepts and fundamental knowledge",
        "medium": "intermediate concepts requiring some analysis",
        "hard": "advanced concepts requiring deep understanding and critical thinking"
    }

    question_type_map = {
        "multiple-choice": "Each question should have 4 multiple choice options (A, B, C, D).",
        "true-false": "Each question should be a true/false question with only 2 options: 'True' and 'False'.",
        "mixed": "Mix of multiple choice (4 options) and true/false questions."
    }

    return f"""
Generate a quiz about "{topic}" with the following specifications:
- Difficulty: {difficulty} ({difficulty_map.get(difficulty, '')})
- Number of questions: {question_count}
- Question type: {question_type_map.get(question_type, '')}

Requirements:
1. Create {question_count} high-quality questions
2. Questions should be clear, unambiguous, and test understanding
3. For multiple choice questions, provide exactly 4 options
4. For true/false questions, provide exactly 2 options: "True" and "False"
5. Include brief explanations for the correct answers
6. Ensure correct answers are accurate and well-researched
7. Distribute correct answers evenly across options (for multiple choice)

Return the response in this exact JSON format:
{{
    "topic": "{topic}",
    "difficulty": "{difficulty}",
    "questions": [
        {{
            "question": "Question text here?",
            "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
            "correct_answer": "Option 1",
            "explanation": "Brief explanation of why this is correct"
        }}
    ]
}}
"""

async def generate_quiz_logic(request: QuizRequest) -> QuizResponse:
    if not request.topic.strip():
        raise HTTPException(status_code=400, detail="Topic cannot be empty")

    if not (1 <= request.question_count <= 50):
        raise HTTPException(status_code=400, detail="Question count must be between 1 and 50")

    prompt = generate_quiz_prompt(request.topic, request.difficulty, request.question_count, request.question_type)
    response_text = await get_gemini_model_response(prompt)

    if not response_text:
        raise HTTPException(status_code=500, detail="No response from AI model")

    cleaned = clean_json_response(response_text)

    try:
        quiz_data = json.loads(cleaned)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON response from AI model")

    processed_questions = []
    for i, q in enumerate(quiz_data.get("questions", [])):
        if not all(k in q for k in ["question", "options", "correct_answer"]):
            raise HTTPException(status_code=500, detail=f"Invalid format in question {i}")
        if q["correct_answer"] not in q["options"]:
            q["correct_answer"] = q["options"][0]
        processed_questions.append(QuizQuestion(**q))

    quiz = Quiz(
        topic=quiz_data.get("topic", request.topic),
        difficulty=quiz_data.get("difficulty", request.difficulty),
        questions=processed_questions
    )
    return QuizResponse(quiz=quiz)
