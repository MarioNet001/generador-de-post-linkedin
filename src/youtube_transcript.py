import os
import re
import requests
import http.cookiejar
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
from .utils import setup_logger

load_dotenv()
logger = setup_logger("transcript_service")

def extract_video_id(url):
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    return match.group(1) if match else None

def clean_transcript(text):
    """Elimina ruido común de las transcripciones de YouTube."""
    text = re.sub(r'\[Música\]|\[Aplausos\]|\[Music\]', '', text, flags=re.IGNORECASE)
    return re.sub(r'\s+', ' ', text).strip()

def smart_slice(text, max_chars=10000):
    """Si el texto es muy largo, prioriza inicio y fin."""
    if len(text) <= max_chars:
        return text
    head = text[:int(max_chars * 0.7)]
    tail = text[-int(max_chars * 0.3):]
    logger.info(f"✂️ Slicing aplicado: {len(text)} -> {max_chars}")
    return f"{head}\n\n[...]\n\n{tail}"

def get_yt_transcript(video_url):
    """Obtiene y optimiza la transcripción de YouTube."""
    video_id = extract_video_id(video_url)
    if not video_id: raise ValueError(f"URL inválida: {video_url}")

    cookies_file = 'cookies.txt'
    http_client = None
    if os.path.exists(cookies_file):
        try:
            session = requests.Session()
            session.cookies = http.cookiejar.MozillaCookieJar(cookies_file)
            session.cookies.load(ignore_discard=True, ignore_expires=True)
            http_client = session
        except Exception as e:
            logger.warning(f"Error cookies: {e}")
    
    raw_text = ""
    try:
        yt_api = YouTubeTranscriptApi(http_client=http_client)
        data = yt_api.fetch(video_id, languages=['es', 'en'])
        raw_text = " ".join([item.text for item in data])
    except Exception:
        try:
            data = YouTubeTranscriptApi(http_client=http_client).fetch(video_id)
            raw_text = " ".join([item.text for item in data])
        except Exception as e:
            raise Exception(f"Error transcripción: {e}")
            
    return smart_slice(clean_transcript(raw_text))
