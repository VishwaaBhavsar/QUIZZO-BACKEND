# from fastapi import APIRouter, UploadFile, File, HTTPException
# from services.image_service import extract_text_from_image

# router = APIRouter()

# @router.post("/upload-image")
# async def upload_image(file: UploadFile = File(...)):
#     if not file.content_type.startswith("image/"):
#         raise HTTPException(status_code=400, detail="Only image files are allowed")
#     content = await file.read()
#     text = extract_text_from_image(content)
#     return {"text": text}
# Add this code to your Python backend
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List
from services.image_service import extract_text_from_image
from services.quiz_service import generate_quiz_logic
from models.request import QuizRequest
router = APIRouter()

# @router.post("/generate-quiz-from-image") # This is our "Head Chef"
# async def generate_quiz_from_image(
#     files: List[UploadFile] = File(...), 
#     difficulty: str = Form(...),
#     question_count: int = Form(...),
#     question_type: str = Form(...)
# ):
#     try:
#         # Step 1: Get text from the image (using your old service)
#         combined_text = ""
#         for file in files:
#             content = await file.read()
#             text = extract_text_from_image(content)
#             combined_text += text + "\n"

#         # Step 2: Make a quiz from that text (using your other service)
#         quiz_data = await generate_quiz_logic(
#             topic=combined_text,
#             difficulty=difficulty,
#             question_count=question_count,
#             question_type=question_type
#         )
        
#         # Step 3: Give the final quiz back to React
#         return {"quiz": quiz_data}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Internal server error")
import traceback

@router.post("/generate-quiz-from-image")
async def generate_quiz_from_image(
    files: List[UploadFile] = File(...), 
    difficulty: str = Form(...),
    question_count: int = Form(...),
    question_type: str = Form(...)
):
    try:
        combined_text = ""
        for file in files:
            content = await file.read()
            text = extract_text_from_image(content)
            combined_text += text + "\n"

        quiz_data = await generate_quiz_logic(
            QuizRequest(
            topic=combined_text,
            difficulty=difficulty,
            question_count=question_count,
            question_type=question_type
            )
        )

        return {"quiz": quiz_data}
    
    except Exception as e:
        traceback.print_exc()  # This shows the full error in terminal
        raise HTTPException(status_code=500, detail=str(e))  # Send the actual error to frontend
