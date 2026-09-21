import os
from dotenv import load_dotenv

load_dotenv()

def get_gemini_api_key():

    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY not found. Check that your .env file exists "
            "and contains a line like: GEMINI_API_KEY=your_key_here"
        )

    return api_key
