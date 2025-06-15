from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.ai_service import get_gemini_model_response
from db.supabase import supabase
import json
import re
from datetime import datetime 

router = APIRouter()

class TextInput(BaseModel):
    prompt: str
    source_type: str = "text"  # optional, defaults to "text"

@router.post("/")
async def generate_flashcards_from_text(data: TextInput):
    try:
        prompt = f"""
        Convert the following study material into multiple flashcards in JSON format:
        [
          {{ "question": "What is ...?", "answer": "..." }},
          ...
        ]

        Study Material:
        {data.prompt}
        """
        raw = await get_gemini_model_response(prompt)
        print("🧠 Raw response from Gemini:", repr(raw))

        def clean_gemini_json(raw: str) -> str:
            return re.sub(r"^```json\s*|\s*```$", "", raw.strip())

        try:
            flashcards = json.loads(clean_gemini_json(raw))
        except json.JSONDecodeError as e:
            print("⚠️ JSON Decode Error:", e)
            raise HTTPException(status_code=500, detail="Invalid JSON from Gemini.")

        # Save to Supabase
        for card in flashcards:
            print("💾 Saving flashcard:", card)
            supabase.table("flashcards").insert({
                "question": card["question"],
                "answer": card["answer"],
                "source_type": data.source_type,
                "created_at":datetime.utcnow().isoformat()
            }).execute()

        return {"data": flashcards}

    except Exception as e:
        print("🔥 SERVER ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))
