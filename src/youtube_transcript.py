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

def get_yt_transcript(video_url):
    """Obtiene la transcripción de YouTube."""
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
    
    try:
        yt_api = YouTubeTranscriptApi(http_client=http_client)
        data = yt_api.fetch(video_id, languages=['es', 'en'])
        return " ".join([item.text for item in data]).strip()
    except Exception:
        try:
            data = YouTubeTranscriptApi(http_client=http_client).fetch(video_id)
            return " ".join([item.text for item in data]).strip()
        except Exception as e:
            raise Exception(f"Error transcripción: {e}")
