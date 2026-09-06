import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is missing from environment variables.")
