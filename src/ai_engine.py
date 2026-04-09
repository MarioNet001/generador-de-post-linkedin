import os
import re
import google.generativeai as genai
from dotenv import load_dotenv
from .utils import setup_logger, retry_operation

load_dotenv()
logger = setup_logger("ai_engine")

@retry_operation(max_retries=3, delay=2, logger=logger)
def generate_linkedin_post(transcript):
    """Genera un post de LinkedIn profesional usando Gemini."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key: raise ValueError("GEMINI_API_KEY no configurado")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-3-flash-preview')

    prompt = f"Eres un experto en LinkedIn. Crea un post basado en:\n{transcript}\nGenera solo el post."
    
    safety_settings = [{"category": c, "threshold": "BLOCK_NONE"} for c in [
        "HARM_CATEGORY_HARASSMENT", "HARM_CATEGORY_HATE_SPEECH", 
        "HARM_CATEGORY_SEXUALLY_EXPLICIT", "HARM_CATEGORY_DANGEROUS_CONTENT"
    ]]

    response = model.generate_content(prompt, safety_settings=safety_settings)
    return response.text.strip()

@retry_operation(max_retries=3, delay=2, logger=logger)
def generate_infographic_content(transcript):
    """Genera esquema de infografía en Markdown."""
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-3-flash-preview')

    prompt = f"Crea un esquema de infografía Markdown para:\n{transcript}"
    response = model.generate_content(prompt)
    return response.text.strip()

@retry_operation(max_retries=3, delay=2, logger=logger)
def generate_infographic_svg(transcript):
    """Genera código SVG visual."""
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-3-flash-preview')

    prompt = f"Genera un SVG vertical (800x1200) básico y limpio para:\n{transcript}\nUsa colores sólidos y emojis. Solo código <svg>."
    response = model.generate_content(prompt)
    
    raw = response.text.strip()
    match = re.search(r'(<svg.*?</svg>)', raw, re.DOTALL | re.IGNORECASE)
    return match.group(1) if match else raw
