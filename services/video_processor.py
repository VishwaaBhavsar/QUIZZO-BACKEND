import re
from typing import Optional
from youtube_transcript_api import YouTubeTranscriptApi
from utils.logger import setup_logger
from utils.exceptions import VideoProcessingError

logger = setup_logger(__name__)

class VideoProcessor:
    """Handle video content processing, primarily YouTube videos"""
    
    @staticmethod
    def extract_youtube_video_id(url: str) -> Optional[str]:
        """Extract YouTube video ID from various URL formats"""
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
            r'youtube\.com\/v\/([^&\n?#]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    @staticmethod
    def get_youtube_transcript(video_id: str) -> str:
        """Get transcript from YouTube video"""
        try:
            logger.info(f"Fetching transcript for video ID: {video_id}")
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            transcript = " ".join([item['text'] for item in transcript_list])
            logger.info(f"Successfully fetched transcript of length: {len(transcript)}")
            return transcript
        except Exception as e:
            logger.error(f"Error getting YouTube transcript for {video_id}: {e}")
            raise VideoProcessingError(f"Could not get transcript: {str(e)}")
    
    @classmethod
    def process_video_url(cls, url: str) -> str:
        """Process video URL and return transcript"""
        video_id = cls.extract_youtube_video_id(url)
        if not video_id:
            raise VideoProcessingError("Invalid YouTube URL format")
        
        return cls.get_youtube_transcript(video_id)
    
    @classmethod
    def validate_video_url(cls, url: str) -> dict:
        """Validate if a video URL is supported and can provide transcript"""
        try:
            video_id = cls.extract_youtube_video_id(url)
            
            if not video_id:
                return {"valid": False, "message": "Invalid YouTube URL format"}
            
            # Check if transcript is available
            try:
                transcript = cls.get_youtube_transcript(video_id)
                return {
                    "valid": True, 
                    "message": "Video transcript available",
                    "transcript_length": len(transcript)
                }
            except VideoProcessingError:
                return {"valid": False, "message": "No transcript available for this video"}
                
        except Exception as e:
            logger.error(f"Error validating video URL: {e}")
            return {"valid": False, "message": f"Error validating URL: {str(e)}"}