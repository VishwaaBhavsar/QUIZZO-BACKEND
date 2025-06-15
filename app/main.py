
# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import google.generativeai as genai
# import json
# import os
# from typing import List, Optional
# import re
# from dotenv import load_dotenv
# load_dotenv()

# # Initialize FastAPI app
# app = FastAPI(title="AI Quiz Generator API", version="1.0.0")

# # Configure CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],  # React app URL
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Configure Gemini API
# # Set your API key as environment variable: export GEMINI_API_KEY=your_api_key_here
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# if not GEMINI_API_KEY:
#     raise ValueError("GEMINI_API_KEY environment variable is required")

# genai.configure(api_key=GEMINI_API_KEY)
# model = genai.GenerativeModel('gemini-1.5-flash')

# # Pydantic models
# class QuizRequest(BaseModel):
#     topic: str
#     difficulty: str = "medium"
#     question_count: int = 5
#     question_type: str = "multiple-choice"

# class QuizQuestion(BaseModel):
#     question: str
#     options: List[str]
#     correct_answer: str
#     explanation: Optional[str] = None

# class Quiz(BaseModel):
#     topic: str
#     difficulty: str
#     questions: List[QuizQuestion]

# class QuizResponse(BaseModel):
#     quiz: Quiz

# def clean_json_response(text: str) -> str:
#     """Clean and extract JSON from Gemini response"""
#     # Remove code block markers if present
#     text = re.sub(r'```json\s*', '', text)
#     text = re.sub(r'```\s*$', '', text)
    
#     # Find JSON content between braces
#     json_match = re.search(r'\{.*\}', text, re.DOTALL)
#     if json_match:
#         return json_match.group(0)
    
#     return text.strip()

# def generate_quiz_prompt(topic: str, difficulty: str, question_count: int, question_type: str) -> str:
#     """Generate the prompt for Gemini API"""
    
#     difficulty_descriptions = {
#         "easy": "basic concepts and fundamental knowledge",
#         "medium": "intermediate concepts requiring some analysis",
#         "hard": "advanced concepts requiring deep understanding and critical thinking"
#     }
    
#     question_type_instructions = {
#         "multiple-choice": "Each question should have 4 multiple choice options (A, B, C, D).",
#         "true-false": "Each question should be a true/false question with only 2 options: 'True' and 'False'.",
#         "mixed": "Mix of multiple choice (4 options) and true/false questions."
#     }
    
#     prompt = f"""
# Generate a quiz about "{topic}" with the following specifications:
# - Difficulty: {difficulty} ({difficulty_descriptions.get(difficulty, '')})
# - Number of questions: {question_count}
# - Question type: {question_type_instructions.get(question_type, '')}

# Requirements:
# 1. Create {question_count} high-quality questions
# 2. Questions should be clear, unambiguous, and test understanding
# 3. For multiple choice questions, provide exactly 4 options
# 4. For true/false questions, provide exactly 2 options: "True" and "False"
# 5. Include brief explanations for the correct answers
# 6. Ensure correct answers are accurate and well-researched
# 7. Distribute correct answers evenly across options (for multiple choice)

# Return the response in this exact JSON format:
# {{
#     "topic": "{topic}",
#     "difficulty": "{difficulty}",
#     "questions": [
#         {{
#             "question": "Question text here?",
#             "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
#             "correct_answer": "Option 1",
#             "explanation": "Brief explanation of why this is correct"
#         }}
#     ]
# }}

# Make sure the JSON is valid and properly formatted. Do not include any text outside the JSON structure.
# """
    
#     return prompt

# @app.get("/")
# async def root():
#     return {"message": "AI Quiz Generator API is running!"}

# @app.post("/generate-quiz", response_model=QuizResponse)
# async def generate_quiz(request: QuizRequest):
#     try:
#         # Validate request
#         if not request.topic.strip():
#             raise HTTPException(status_code=400, detail="Topic cannot be empty")
        
#         if request.question_count < 1 or request.question_count > 50:
#             raise HTTPException(status_code=400, detail="Question count must be between 1 and 50")
        
#         # Generate prompt
#         prompt = generate_quiz_prompt(
#             request.topic, 
#             request.difficulty, 
#             request.question_count, 
#             request.question_type
#         )
        
#         # Call Gemini API
#         response = model.generate_content(prompt)
        
#         if not response.text:
#             raise HTTPException(status_code=500, detail="No response from AI model")
        
#         # Clean and parse JSON response
#         cleaned_response = clean_json_response(response.text)
        
#         try:
#             quiz_data = json.loads(cleaned_response)
#         except json.JSONDecodeError as e:
#             print(f"JSON decode error: {e}")
#             print(f"Raw response: {response.text}")
#             print(f"Cleaned response: {cleaned_response}")
#             raise HTTPException(status_code=500, detail="Invalid JSON response from AI model")
        
#         # Validate quiz structure
#         if "questions" not in quiz_data:
#             raise HTTPException(status_code=500, detail="Invalid quiz format: missing questions")
        
#         # Process questions to ensure proper format
#         processed_questions = []
#         for i, q in enumerate(quiz_data["questions"]):
#             if not all(key in q for key in ["question", "options", "correct_answer"]):
#                 raise HTTPException(status_code=500, detail=f"Invalid question format at index {i}")
            
#             # Ensure correct_answer is in options
#             if q["correct_answer"] not in q["options"]:
#                 print(f"Warning: Correct answer not in options for question {i+1}")
#                 # Try to find the closest match or use the first option
#                 q["correct_answer"] = q["options"][0]
            
#             processed_questions.append(QuizQuestion(**q))
        
#         quiz = Quiz(
#             topic=quiz_data.get("topic", request.topic),
#             difficulty=quiz_data.get("difficulty", request.difficulty),
#             questions=processed_questions
#         )
        
#         return QuizResponse(quiz=quiz)
        
#     except HTTPException:
#         raise
#     except Exception as e:
#         print(f"Unexpected error: {e}")
#         raise HTTPException(status_code=500, detail="Internal server error")

# @app.get("/health")
# async def health_check():
#     return {"status": "healthy", "service": "AI Quiz Generator API"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import quiz, health,image,text_flashcard
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI Quiz Generator API", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Update with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(quiz.router, prefix="/generate-quiz", tags=["Quiz"])
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(image.router,prefix="/api/image",tags=["Image"])
app.include_router(text_flashcard.router,prefix='/generate-flashcard')

@app.get("/")
async def root():
    return {"message": "AI Quiz Generator API is running!"}
