"""
llm_client.py

The only file in this project that talks directly to the Gemini API.
Every other file (personas.py, judge.py) calls get_response() instead
of touching the Google SDK themselves.
"""

from google import genai
from google.genai import types
from config import get_gemini_api_key

_client = genai.Client(api_key=get_gemini_api_key())

MODEL_NAME = "gemini-3.5-flash-lite"


def get_response(prompt, system_instruction=None):
    """
    Sends a prompt to Gemini and returns its text reply as a string.
    """
    config = types.GenerateContentConfig(
        system_instruction=system_instruction
    )

    response = _client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=config,
    )

    return response.text
