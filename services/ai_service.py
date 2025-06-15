import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is required")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

async def get_gemini_model_response(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text if response and response.text else ""
