# import os
# from typing import List
# from pydantic_settings import BaseSettings
# from dotenv import load_dotenv

# load_dotenv()

# class Settings(BaseSettings):
#     # API Keys
#     gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    
#     # App Configuration
#     app_name: str = os.getenv("APP_NAME", "AI Quiz Generator API")
#     app_version: str = os.getenv("APP_VERSION", "1.0.0")
#     debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    
#     # Server Configuration
#     host: str = os.getenv("HOST", "0.0.0.0")
#     port: int = int(os.getenv("PORT", "8000"))
    
#     # CORS Configuration
#     allowed_origins: List[str] = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
    
#     # Content Limits
#     max_content_length: int = int(os.getenv("MAX_CONTENT_LENGTH", "10000"))
#     min_content_length: int = int(os.getenv("MIN_CONTENT_LENGTH", "100"))
    
#     # Gemini Configuration
#     gemini_model: str = "gemini-1.5-flash"
#     gemini_temperature: float = 0.7
#     gemini_max_output_tokens: int = 2048

#     class Config:
#         env_file = ".env"

# settings = Settings()
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    gemini_api_key: str = ""
    app_name: str = "AI Quiz Generator API"
    app_version: str = "1.0.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    allowed_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    max_content_length: int = 10000
    min_content_length: int = 100
    gemini_model: str = "gemini-1.5-flash"
    gemini_temperature: float = 0.7
    gemini_max_output_tokens: int = 2048

    @property
    def cors_origins(self) -> List[str]:
        """Convert comma-separated origins string to list"""
        return [origin.strip() for origin in self.allowed_origins.split(',')]

    model_config = {
        "env_file": ".env"
    }

settings = Settings()