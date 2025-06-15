from fastapi import APIRouter

router = APIRouter()

@router.get("")
async def health_check():
    return {"status": "healthy", "service": "AI Quiz Generator API"}
