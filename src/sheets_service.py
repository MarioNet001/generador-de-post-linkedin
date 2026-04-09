import os
import requests
import datetime
from dotenv import load_dotenv

load_dotenv()

def append_to_sheet_via_webhook(title, post_content):
    """Guarda en Google Sheets vía Webhook."""
    webhook_url = os.getenv("WEBHOOK_URL")
    if not webhook_url: return None

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payload = {"fecha": now, "titulo": title, "post": post_content}

    response = requests.post(webhook_url, json=payload)
    return response.text if response.status_code == 200 else None
