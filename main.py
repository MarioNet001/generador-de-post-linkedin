import sys
import os
from dotenv import load_dotenv

from src.youtube_transcript import get_yt_transcript
from src.ai_engine import generate_linkedin_post
from src.excel_storage import save_to_local_excel

load_dotenv()

def run_pipeline(video_url):
    """Ejecuta el flujo completo vía CLI."""
    print(f"\n--- Procesando: {video_url} ---")
    
    try:
        transcript = get_yt_transcript(video_url)
        print(f"Transcripción obtenida ({len(transcript)} chars).")

        print("Generando post con Gemini...")
        post = generate_linkedin_post(transcript)
        
        print("\n--- POST GENERADO ---")
        print(post)

        print("\nGuardando en Excel local...")
        path = save_to_local_excel(f"Video: {video_url}", post)
        print(f"Archivo guardado en: {path}")

    except Exception as e:
        print(f"\n[ERROR]: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python main.py <URL_YOUTUBE>")
    else:
        run_pipeline(sys.argv[1])
