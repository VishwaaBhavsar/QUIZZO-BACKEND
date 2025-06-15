from functools import lru_cache
from services.quiz_service import QuizGenerator
from backend.services.ai_service import ContentProcessor
from services.video_processor import VideoProcessor

@lru_cache()
def get_quiz_generator() -> QuizGenerator:
    """Dependency to get QuizGenerator instance"""
    return QuizGenerator()

@lru_cache()
def get_content_processor() -> ContentProcessor:
    """Dependency to get ContentProcessor instance"""
    return ContentProcessor()

@lru_cache()
def get_video_processor() -> VideoProcessor:
    """Dependency to get VideoProcessor instance"""
    return VideoProcessor()