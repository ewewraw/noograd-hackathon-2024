import os
from dotenv import load_dotenv

load_dotenv()

GMAIL_API_KEY = os.getenv("GMAIL_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")